import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

ROLES = [
    "Software Engineer", "Data Scientist", "Product Manager",
    "UX Designer", "DevOps Engineer", "Marketing Manager",
    "Financial Analyst", "HR Business Partner",
    "Project Manager", "Business Analyst"
]

ROLE_SKILL_MAP = {
    "Software Engineer":   ["python","javascript","java","react","sql","git","html","css"],
    "Data Scientist":      ["python","machine learning","statistics","data analysis","tableau","tensorflow","pandas"],
    "Product Manager":     ["agile","scrum","leadership","stakeholder","presentation","project management"],
    "UX Designer":         ["figma","ux","ui","design thinking","presentation","communication"],
    "DevOps Engineer":     ["aws","docker","kubernetes","linux","git","python"],
    "Marketing Manager":   ["seo","social media","content","branding","communication","presentation"],
    "Financial Analyst":   ["accounting","financial analysis","forecasting","statistics","excel","sap"],
    "HR Business Partner": ["leadership","communication","stakeholder","presentation","negotiation"],
    "Project Manager":     ["project management","agile","leadership","scrum","stakeholder","communication"],
    "Business Analyst":    ["data analysis","sql","stakeholder","presentation","agile","excel"],
}

EXPERIENCE_BOOST = {
    "Software Engineer": 0,   "Data Scientist": 2,
    "Product Manager": 3,     "UX Designer": 0,
    "DevOps Engineer": 2,     "Marketing Manager": 2,
    "Financial Analyst": 0,   "HR Business Partner": 3,
    "Project Manager": 3,     "Business Analyst": 2,
}


class RoleSyncModel:
    def train(self):
        pass  # Rule-based, no training needed

    def predict(self, employee_profile):
        skills = [s.lower() for s in employee_profile.get("skills", [])]
        experience = employee_profile.get("experience_years", 0)
        performance = employee_profile.get("performance_score", 5.0)

        scores = {}
        for role, role_skills in ROLE_SKILL_MAP.items():
            matched = sum(1 for s in skills if s in role_skills)
            total = len(role_skills)
            skill_score = (matched / total) * 70

            exp_required = EXPERIENCE_BOOST[role]
            exp_diff = abs(experience - exp_required)
            exp_score = max(0, 20 - (exp_diff * 2))

            perf_score = (performance / 10) * 10

            scores[role] = round(skill_score + exp_score + perf_score, 1)

        sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        top_score = sorted_roles[0][1] if sorted_roles[0][1] > 0 else 1
        recommendations = []
        for role, score in sorted_roles[:3]:
            confidence = round((score / top_score) * 85 + 5, 1)
            confidence = min(confidence, 95.0)
            recommendations.append({"role": role, "confidence": confidence})

        return recommendations


rolesync_model = RoleSyncModel()