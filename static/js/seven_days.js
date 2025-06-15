document.addEventListener("DOMContentLoaded", function () {
  const sevenDayModal = new bootstrap.Modal(
    document.getElementById("sevenDayModal")
  );
  const openBtn = document.getElementById("openSevenDaysModal");
  const form = document.getElementById("sevenDayForm");

  openBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const projectId = this.dataset.projectId;
    document.getElementById("projectIdInput").value = projectId;
    form.reset();
    sevenDayModal.show();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const url = openBtn.dataset.url;

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
          showToast("SevenDays created successfully!", "success");

          // Hide the modal and reload the page after showing the success toast
          sevenDayModal.hide();

          setTimeout(function () {
            location.reload(); // Reload after the toast disappears
          }, 3000); // Adjust timeout if you want the page to reload sooner or later
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
  const sevenDayModal = new bootstrap.Modal(
    document.getElementById("sevenDayModalEdit")
  );

  $(".openEditSevenDaysModal").on("click", function () {
    const url = $(this).data("url");
    $.get(url, function (res) {
      $("#sevenDayModalContent").html(res);
      sevenDayModal.show();
    }).fail(function () {
      alert("Failed to load edit form.");
    });
  });

  $(".openDeleteSevenDaysModal").on("click", function () {
    const url = $(this).data("url");
    $.get(url, function (res) {
      $("#sevenDayModalContent").html(res);
      sevenDayModal.show();
    }).fail(function () {
      alert("Failed to load delete confirmation.");
    });
  });
});
