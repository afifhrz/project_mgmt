$(document).ready(function () {
  $("#update-task-form").on("submit", function (e) {
    e.preventDefault();
    const formData = $(this).serialize();

    $.ajax({
      url: updateTaskUrl, // You need to implement this view
      type: "POST",
      data: formData,
      success: function (response) {
        if (response.success) {
          showToast("Task updated successfully", "success");
          setTimeout(function () {
            location.reload(); // or any other follow-up logic
          }, 3000);
        } else {
          showToast("Failed to update task", "danger");
        }
      },
      error: function () {
        showToast("An error occurred while updating the task", "danger");
      },
    });
  });
});

$(document).ready(function () {
  $("#edit-btn").click(function () {
    const form = $("#edit-form");
    const role = $("body").data("role");

    // Toggle read-only fields
    $("#edit-form input, #edit-form select, #edit-form textarea")
      .not(".no-edit")
      .each(function () {
        const $field = $(this);
        const name = $field.attr("name");
        const type = $field.attr("type");
        const tag = $field.prop("tagName").toLowerCase();

        if (role === "Person In Charge") {
          // Only make unattained_reason editable, others readonly/disabled
          if (name === "unattained_reason") {
            if (type === "checkbox" || type === "radio" || tag === "select") {
              $field.prop("disabled", false);
            } else {
              $field.prop("readonly", false);
            }
          } else {
            if (type === "checkbox" || type === "radio" || tag === "select") {
              $field.prop("disabled", true);
            } else {
              $field.prop("readonly", true);
            }
          }
        } else {
          // For other roles, toggle as before (enable if disabled, disable if enabled)
          if (type === "checkbox" || type === "radio" || tag === "select") {
            $field.prop("disabled", !$field.prop("disabled"));
          } else {
            $field.prop("readonly", !$field.prop("readonly"));
          }
        }
      });

    // Toggle button visibility
    $("#save-btn").toggleClass("d-none");
    $(this).toggleClass("btn-outline-primary btn-secondary");
    $(this).text(function (_, text) {
      return text.trim() === "✏️ Edit" ? "❌ Cancel" : "✏️ Edit";
    });
  });

  $("#save-btn").click(function (e) {
    // Submit the form via AJAX or standard post — adjust to your needs
    showToast("Saving", "info");
    const role = $("body").data("role");

    e.preventDefault();
    const form = $("#edit-form")[0];
    const formData = new FormData(form);

    $.ajax({
      url: updateTaskUrl,
      type: "POST",
      headers: {
        "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val(),
      },
      data: formData,
      processData: false, // Important to avoid query string encoding
      contentType: false, // Let the browser set it, including multipart boundary
      success: function (response) {
        if (response.success) {
          // Optionally, return to read-only mode
          $("#edit-form input, #edit-form select, #edit-form textarea").each(
            function () {
              const $field = $(this);
              const name = $field.attr("name");
              const type = $field.attr("type");
              const tag = $field.prop("tagName").toLowerCase();

              if (role === "Person In Charge") {
                if (name === "unattained_reason") {
                  // Keep unattained_reason editable (readonly false / disabled false)
                  if (
                    type === "checkbox" ||
                    type === "radio" ||
                    tag === "select"
                  ) {
                    $field.prop("disabled", false);
                  } else {
                    $field.prop("readonly", false);
                  }
                } else {
                  // All other fields readonly/disabled
                  if (
                    type === "checkbox" ||
                    type === "radio" ||
                    tag === "select"
                  ) {
                    $field.prop("disabled", true);
                  } else {
                    $field.prop("readonly", true);
                  }
                }
              } else {
                // For other roles, all fields readonly/disabled
                if (
                  type === "checkbox" ||
                  type === "radio" ||
                  tag === "select"
                ) {
                  $field.prop("disabled", true);
                } else {
                  $field.prop("readonly", true);
                }
              }
            }
          );
          $("#edit-btn")
            .removeClass("btn-secondary")
            .addClass("btn-outline-primary")
            .text("✏️ Edit");
          $(this).addClass("d-none");
          showToast("Task updated successfully", "success");

          // Optional delay then reload
          setTimeout(() => {
            location.reload();
          }, 3000);
        } else {
          showToast("Failed to update task", "danger");
        }
      },
      error: function () {
        showToast("An error occurred while updating the task", "danger");
      },
    });
  });
});
