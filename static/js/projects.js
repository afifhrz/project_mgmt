$(document).ready(function () {
    let postUrl = '';
  
    // Show modal and capture URL
    $('#openProjectModal').on('click', function () {
      postUrl = $(this).data('url');
      $('#projectModal').modal('show');
    });
  
    // Submit form via AJAX
    $('#projectCreateForm').on('submit', function (e) {
      e.preventDefault();
      const data = $(this).serialize();
  
      $.ajax({
        type: 'POST',
        url: postUrl,
        data: data,
        success: function (response) {
          $('#projectModal').modal('hide');
          $('#projectCreateForm')[0].reset();
          location.reload(); // or reload project list dynamically
        },
        error: function (xhr) {
          alert(xhr.responseJSON?.error || 'An error occurred.');
        }
      });
    });
  });
  