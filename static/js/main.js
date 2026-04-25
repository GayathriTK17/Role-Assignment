document.addEventListener('DOMContentLoaded', function () {

  // ---- File upload display ----
  const fileInput = document.getElementById('resume');
  const fileNameDisplay = document.getElementById('file-name-display');
  const uploadArea = document.querySelector('.file-upload-area');

  if (fileInput && fileNameDisplay) {
    fileInput.addEventListener('change', function () {
      if (this.files.length > 0) {
        fileNameDisplay.textContent = this.files[0].name;
        fileNameDisplay.style.display = 'block';
      } else {
        fileNameDisplay.textContent = '';
      }
    });
  }

  if (uploadArea) {
    uploadArea.addEventListener('dragover', e => {
      e.preventDefault();
      uploadArea.classList.add('drag-over');
    });
    uploadArea.addEventListener('dragleave', () => {
      uploadArea.classList.remove('drag-over');
    });
    uploadArea.addEventListener('drop', e => {
      uploadArea.classList.remove('drag-over');
    });
  }

  // ---- Animate confidence bars ----
  const bars = document.querySelectorAll('.conf-bar-fill');
  setTimeout(() => {
    bars.forEach(bar => {
      const width = bar.dataset.width;
      if (width) bar.style.width = width + '%';
    });
  }, 300);

  // ---- Feedback modal ----
  const feedbackBtn = document.getElementById('feedback-btn');
  const feedbackModal = document.getElementById('feedback-modal');
  const modalClose = document.getElementById('modal-close');
  const feedbackForm = document.getElementById('feedback-form');

  if (feedbackBtn && feedbackModal) {
    feedbackBtn.addEventListener('click', () => {
      feedbackModal.classList.add('open');
    });

    modalClose?.addEventListener('click', () => {
      feedbackModal.classList.remove('open');
    });

    feedbackModal.addEventListener('click', (e) => {
      if (e.target === feedbackModal) feedbackModal.classList.remove('open');
    });
  }

  if (feedbackForm) {
    feedbackForm.addEventListener('submit', async function (e) {
      e.preventDefault();
      const data = {
        name: document.getElementById('fb-name')?.value,
        recommended_role: document.getElementById('fb-recommended')?.value,
        actual_role: document.getElementById('fb-actual')?.value,
        satisfaction: document.getElementById('fb-satisfaction')?.value
      };

      try {
        const res = await fetch('/api/feedback', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        const result = await res.json();
        feedbackModal.classList.remove('open');
        showToast('Feedback submitted. Thank you!');
      } catch (err) {
        showToast('Could not submit feedback.', true);
      }
    });
  }

  // ---- Range input live display ----
  const rangeInputs = document.querySelectorAll('input[type="range"]');
  rangeInputs.forEach(input => {
    const display = document.getElementById(input.id + '-display');
    if (display) {
      display.textContent = input.value;
      input.addEventListener('input', () => { display.textContent = input.value; });
    }
  });

  // ---- Toast notification ----
  function showToast(message, isError = false) {
    const existing = document.querySelector('.toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed; bottom: 2rem; right: 2rem; z-index: 999;
      background: ${isError ? '#f5e8e0' : '#e0f0ec'};
      color: ${isError ? '#c9856a' : '#7a9e8a'};
      border: 1px solid ${isError ? '#c9856a' : '#7a9e8a'};
      border-radius: 12px; padding: 12px 20px;
      font-size: 0.88rem; font-weight: 500;
      box-shadow: 0 4px 20px rgba(42,36,32,0.12);
      animation: toastIn 0.3s ease;
    `;

    const style = document.createElement('style');
    style.textContent = '@keyframes toastIn { from { opacity:0; transform:translateY(8px);} to { opacity:1; transform:translateY(0);} }';
    document.head.appendChild(style);
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3500);
  }

  // ---- Form validation ----
  const mainForm = document.getElementById('employee-form');
  if (mainForm) {
    mainForm.addEventListener('submit', function (e) {
      const name = document.getElementById('name')?.value.trim();
      if (!name) {
        e.preventDefault();
        showToast('Please enter the employee name.', true);
        document.getElementById('name')?.focus();
        return;
      }
      const submitBtn = mainForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.textContent = 'Analyzing...';
        submitBtn.disabled = true;
      }
    });
  }
});