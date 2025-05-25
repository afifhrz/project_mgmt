let table;

function loadAssignments(projectId) {
  $.ajax({
    url: `/projects/api/assignments/${projectId}/`,
    method: "GET",
    success: function (data) {
      if (!table) {
        table = new Tabulator("#assignmentTable", {
          layout: "fitColumns",
          columns: [
            { title: "Name", field: "name" },
            { title: "Email", field: "email" },
            {
              title: "Action",
              formatter: function () {
                return `<button class="btn btn-sm btn-danger unassign-btn">Unassign</button>`;
              },
              cellClick: function (e, cell) {
                const userId = cell.getRow().getData().id;
                const projectId = $("#projectSelect").val();
                unassignUser(projectId, userId);
              },
            },
          ],
        });
      }
      else {
        table.setData(data);
      }

      if (data.length === 0) {
        table.replaceData([]);
        table.clearData();
        $("#assignmentTable").find(".tabulator-tableHolder").hide();
        $("#assignmentTable").append(
          '<div class="text-center text-muted bg-white p-3">No PIC assigned to this project.</div>'
        );
      } else {
        $("#assignmentTable").find(".text-muted").remove();
        $("#assignmentTable").find(".tabulator-tableHolder").show();
        table.replaceData(data);
      }
    },
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
