let dataTable;

function loadAssignments(projectId) {
  $.ajax({
    url: `/projects/api/assignments/${projectId}/`,
    method: "GET",

    beforeSend: function () {
      showLoading();
    },

    success: function (data) {
      if (!dataTable) {
        dataTable = $("#assignmentTable").DataTable({
          data: data,
          columns: [
            { title: "Name", data: "name" },
            { title: "Email", data: "email" },
            {
              title: "Action",
              data: null,
              orderable: false,
              searchable: false,
              render: function () {
                return `<button class="btn btn-sm btn-danger unassign-btn">Unassign</button>`;
              }
            }
          ],
          dom: 't', // Hide default UI if needed
          autoWidth: false
        });

        // Delegate event listener to dynamic buttons
        $('#assignmentTable tbody').on('click', '.unassign-btn', function () {
          const rowData = dataTable.row($(this).closest('tr')).data();
          const userId = rowData.id;
          const projectId = $("#projectSelect").val();
          unassignUser(projectId, userId);
        });

      } else {
        dataTable.clear().rows.add(data).draw();
      }

      // Handle empty state
      if (data.length === 0) {
        $("#assignmentTable_wrapper").hide(); // hide DataTable
        if ($("#noDataMessage").length === 0) {
          $("#assignmentTable").after(
            '<div id="noDataMessage" class="text-center text-muted bg-white p-3">No PIC assigned to this project.</div>'
          );
        }
      } else {
        $("#noDataMessage").remove();
        $("#assignmentTable_wrapper").show();
      }
    },

    complete: function () {
      setTimeout(() => hideLoading(), loadingTimeout);
    },

    error: function () {
      $("#assignmentTable").after(
        '<div class="text-danger text-center p-2">Failed to load assignments.</div>'
      );
    }
  });
}

function unassignUser(projectId, userId) {
  $.ajax({
    url: window.location.href,
    type: "POST",
    data: {
      action: "unassign",
      project_id: projectId,
      user_id: userId,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function () {
      showToast("User unassigned successfully.", "success");
      loadAssignments(projectId);
    },
    error: function () {
      showToast("Failed to unassign user.", "danger");
    },
  });
}

$("#projectSelect").on("change", function () {
  const projectId = $(this).val();
  if (projectId != "") {
    loadAssignments(projectId);
  } else {
    document.getElementById("assignmentTable").hidden = true;
  }
});

$("#assignBtn").on("click", function () {
  const projectId = $("#projectSelect").val();
  const userId = $("#userSelect").val();

  $.ajax({
    type: "POST",
    url: window.location.href,
    data: {
      action: "assign",
      project_id: projectId,
      user_id: userId,
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    },
    success: function () {
      showToast("User assigned successfully.", "success");
      loadAssignments(projectId);
    },
    error: function () {
      showToast("Failed to assign user.", "danger");
    },
  });
});

// Initial load
$(document).ready(function () {
  const projectId = $("#projectSelect").val();
  if (projectId != "") {
    loadAssignments(projectId);
  }
});
