document.addEventListener("DOMContentLoaded", () => {
  const uploadBtn = document.getElementById("upload-btn");
  const feedback = document.getElementById("feedback");
  const form = document.getElementById("resume-form");

  uploadBtn.addEventListener("click", () => {
    const fileInput = document.getElementById("resume-upload");
    const file = fileInput.files[0];

    // Validation
    if (!file) {
      feedback.textContent = "Please choose a file.";
      feedback.style.color = "red";
      return;
    }

    feedback.textContent = "Uploading...";
    feedback.style.color = "blue";

    // AJAX Request to server
    const formData = new FormData(form);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
    .then(response => response.json())
    .then(data => {
      feedback.textContent = data.message;
      feedback.style.color = "green";
    })
    .catch(error => {
      feedback.textContent = "Error: " + error.message;
      feedback.style.color = "red";
    });
  });
});
