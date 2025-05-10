document.addEventListener("DOMContentLoaded", function () {
    const sprintModal = new bootstrap.Modal(document.getElementById('sprintModal'));
    const openBtn = document.getElementById('openSprintModal');
    const form = document.getElementById('sprintForm');
  
    openBtn.addEventListener('click', function (e) {
      e.preventDefault();
      const projectId = this.dataset.projectId;
      document.getElementById('projectIdInput').value = projectId;
      form.reset();
      sprintModal.show();
    });
  
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      const url = openBtn.dataset.url;
  
      $.ajax({
        type: 'POST',
        url: url,
        data: $(form).serialize(),
        success: function (response) {
          sprintModal.hide();
          $('body').append(response);
        },
        error: function (xhr) {
          sprintModal.hide();
          $('body').append(`<script>alert("An error occurred. Please try again.")</script>`);
        }
      });
    });
  });
  