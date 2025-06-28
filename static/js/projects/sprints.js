document.addEventListener("DOMContentLoaded", function () {
  const sprintModal = new bootstrap.Modal(
    document.getElementById("sprintModal")
  );
  const openBtn = document.getElementById("openSprintModal");
  const form = document.getElementById("sprintModalForm");

  openBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const projectId = this.dataset.projectId;
    document.getElementById("projectIdInput").value = projectId;
    form.reset();
    sprintModal.show();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const url = openBtn.dataset.url;
    const sprintType = openBtn.dataset.sprintType;

    $.ajax({
      type: "POST",
      url: url,
      data: $(form).serialize(),
      beforeSend: function () {
        showLoading(); // Show loading indicator
      },
      success: function (response) {
        if (response.status === "success") {
          // Show success toast before reload
          showToast(sprintType + " created successfully!", "success");

          // Hide the modal and reload the page after showing the success toast
          sprintModal.hide();

          setTimeout(function () {
            location.reload(); // Reload after the toast disappears
          }, loadingTimeout); // Adjust timeout if you want the page to reload sooner or later
        } else {
          showToast("Something went wrong.", "danger");
        }
      },
      complete: function () {
        setTimeout(() => hideLoading(), loadingTimeout); // Hide loading indicator
      },
      error: function (xhr) {
        const response = xhr.responseJSON;
        const message = response?.message || "An error occurred.";
        showToast(message, "danger");
      },
    });
  });
});

$(document).ready(function () {
  const sprintEditDeleteModal = new bootstrap.Modal(
    document.getElementById("sprintEditDeleteModal")
  );

  $(".openEditSprintModal").on("click", function () {
    const url = $(this).data("url");
    $.get(url, function (res) {
      $("#sprintEditDeleteModalContent").html(res);
      sprintEditDeleteModal.show();
    }).fail(function () {
      alert("Failed to load edit form.");
    });
  });

  $(".openDeleteSprintModal").on("click", function () {
    const url = $(this).data("url");
    $.get(url, function (res) {
      $("#sprintEditDeleteModalContent").html(res);
      sprintEditDeleteModal.show();
    }).fail(function () {
      alert("Failed to load delete confirmation.");
    });
  });
});
