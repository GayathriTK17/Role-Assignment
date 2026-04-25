import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "rolesync_dev_key_2024")

# MongoDB setup (optional - gracefully degrades)
try:
    from database.db import init_db, mongo
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/rolesync")
    init_db(app)
    DB_AVAILABLE = True
except Exception as e:
    print(f"MongoDB not available: {e}. Running without persistence.")
    DB_AVAILABLE = False

from ml.model import rolesync_model
from ml.nlp_processor import extract_skills_from_resume, build_employee_profile

# Train model on startup
rolesync_model.train()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    stats = {
        "total_employees": 0,
        "roles_assigned": 0,
        "avg_confidence": 0,
        "recent_assignments": []
    }

    if DB_AVAILABLE:
        try:
            employees = list(mongo.db.employees.find().sort("created_at", -1).limit(10))
            stats["total_employees"] = mongo.db.employees.count_documents({})
            stats["roles_assigned"] = mongo.db.employees.count_documents({"recommended_role": {"$exists": True}})

            confidences = [e.get("confidence", 0) for e in employees if "confidence" in e]
            stats["avg_confidence"] = round(sum(confidences) / len(confidences), 1) if confidences else 0
            stats["recent_assignments"] = employees[:5]
        except:
            pass

    return render_template("dashboard.html", stats=stats)


@app.route("/employee/new", methods=["GET", "POST"])
def employee_form():
    if request.method == "POST":
        resume_skills = []

        # Handle optional resume upload
        if "resume" in request.files:
            resume_file = request.files["resume"]
            if resume_file and resume_file.filename:
                resume_text = resume_file.read().decode("utf-8", errors="ignore")
                resume_skills = extract_skills_from_resume(resume_text)

        profile = build_employee_profile(request.form, resume_skills)
        recommendations = rolesync_model.predict(profile)

        if not recommendations:
            recommendations = [{"role": "Business Analyst", "confidence": 45.0}]

        top_recommendation = recommendations[0]
        profile["recommended_role"] = top_recommendation["role"]
        profile["confidence"] = top_recommendation["confidence"]
        profile["all_recommendations"] = recommendations
        profile["created_at"] = datetime.utcnow()

        if DB_AVAILABLE:
            try:
                mongo.db.employees.insert_one(profile)
            except:
                pass

        session["last_profile"] = {
            "name": profile["name"],
            "recommended_role": profile["recommended_role"],
            "confidence": profile["confidence"],
            "all_recommendations": recommendations,
            "skills": profile["skills"],
            "experience_years": profile["experience_years"],
            "performance_score": profile["performance_score"],
            "resume_skills": resume_skills
        }

        return redirect(url_for("result"))

    return render_template("employee_form.html")


@app.route("/result")
def result():
    profile = session.get("last_profile")
    if not profile:
        return redirect(url_for("employee_form"))
    return render_template("result.html", profile=profile)


@app.route("/api/feedback", methods=["POST"])
def feedback():
    data = request.json
    if DB_AVAILABLE:
        try:
            mongo.db.feedback.insert_one({
                "employee_name": data.get("name"),
                "recommended_role": data.get("recommended_role"),
                "actual_role": data.get("actual_role"),
                "satisfaction": data.get("satisfaction"),
                "created_at": datetime.utcnow()
            })
        except:
            pass
    return jsonify({"status": "success", "message": "Feedback recorded"})


@app.route("/api/employees")
def get_employees():
    if not DB_AVAILABLE:
        return jsonify([])
    try:
        employees = list(mongo.db.employees.find({}, {"_id": 0}).limit(20))
        return jsonify(employees)
    except:
        return jsonify([])


if __name__ == "__main__":
    app.run(debug=True, port=5000)