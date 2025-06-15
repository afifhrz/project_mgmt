document.addEventListener("DOMContentLoaded", function () {
  const createTaskForm = document.getElementById("createTaskForm");
  const createTaskModal = new bootstrap.Modal(
    document.getElementById("createTaskModal")
  );
  const createTaskUrl = createTaskForm.dataset.url;

  createTaskForm.addEventListener("submit", function (e) {
    e.preventDefault();

    $.ajax({
      type: "POST",
      url: createTaskUrl,
      data: $(createTaskForm).serialize(),
      beforeSend: function () {
        showLoading(); // Show loading indicator
      },
      success: function () {
        showToast("Task created successfully.", "success");
        createTaskModal.hide();
        setTimeout(function () {
          window.location.reload();
        }, loadingTimeout);
      },
      complete: function () {
        setTimeout(() => hideLoading(), loadingTimeout); // Hide loading indicator
      },
      error: function () {
        alert("Failed to create task. Please try again.");
      },
    });
  });
});
