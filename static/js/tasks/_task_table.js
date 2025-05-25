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
    order: [[5, "asc"]], // ⬅️ Sort by column index 5 ascending
    columnDefs: [
      { targets: [0, 5], className: "text-wrap" },
      { targets: [0, 1, 2, 3, 4, 5], className: "text-start align-middle" },
      { targets: 6, className: "text-center align-middle" },
    ],
    columns: [
      { width: "61%" }, // task name
      { width: "7%" }, // status
      { width: "5%" }, // risk level
      { width: "7%" }, // priority urgency
      { width: "6%" }, // priority impact
      { width: "9%" }, // created
      { width: "5%" }, // actions
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
    const isPlanner = $("body").data("role") === "Project Planner";
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