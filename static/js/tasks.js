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
      success: function () {
        createTaskModal.hide();
        location.reload();
      },
      error: function () {
        alert("Failed to create task. Please try again.");
      },
    });
  });
});

// show unattained_reason textarea only if status is not OPEN
document.addEventListener("DOMContentLoaded", () => {
  const statusSel = document.getElementById("status");
  const wrapper = document.getElementById("unattainedWrapper");
  if (!statusSel) return;

  function toggleReason() {
    wrapper.style.display =
      statusSel.value && statusSel.value !== "OPEN" ? "block" : "none";
  }
  statusSel.addEventListener("change", toggleReason);
  toggleReason(); // initial
});

$(function () {
  $("#tasksTable").DataTable({
    fixedHeader: true,
    scrollX: true, // forces horizontal scroll
    pageLength: 25,
    lengthMenu: [10, 25, 50, 100],
    columnDefs: [
      { targets: [1, 22, 23], className: "text-wrap" }, // wrap long text cols
    ],
    language: {
      search: "_INPUT_",
      searchPlaceholder: "Search tasks...",
    },
  });
});

$(function () {
  const modal = new bootstrap.Modal(document.getElementById("editTaskModal"));

  // 1. open modal
  $("#tasksTable").on("click", ".edit-btn", function () {
    const rawEscaped = $(this).attr("data-json");

    // Replace Unicode escape sequences (\u0022 → ")
    const decodedJson = rawEscaped
      .replace(/\\u0022/g, '"')
      .replace(/\\u000A/g, "") // remove newline chars
      .replace(/\\u002D/g, "-") // optional: handle dash
      .replace(/\\u[0-9A-F]{4}/gi, (match) => {
        return String.fromCharCode(parseInt(match.replace("\\u", ""), 16));
      });

    const task = JSON.parse(decodedJson);
    $("#editTaskId").val(task.id);

    // Populate common fields
    $("#editStatus").val(task.status);
    $("#editUnatt").val(task.unattained_reason || "");

    // Role‑based visibility
    const isPlanner = $("body").data("role") === "project_planner";
    $("#plannerFields").toggle(isPlanner);
    $("#picFields").toggle(!isPlanner || isPlanner); // always show for planner & PIC

    // TODO: populate planner‑only inputs …

    modal.show();
  });

  // 2. submit
  $("#editTaskForm").submit(function (e) {
    e.preventDefault();
    const id = $("#editTaskId").val();
    $.post({
      url: `/tasks/${id}/update/`,
      data: $(this).serialize(),
      headers: { "X-CSRFToken": $("input[name=csrfmiddlewaretoken]").val() },
      success: function (resp) {
        if (resp.success) {
          location.reload(); // simplest: refresh table
        } else {
          alert(resp.message);
        }
      },
      error: () => alert("Server error"),
    });
  });
});
