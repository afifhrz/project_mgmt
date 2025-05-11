document.addEventListener("DOMContentLoaded", function () {
  const toastElList = [].slice.call(document.querySelectorAll(".toast"));
  toastElList.forEach(function (toastEl) {
    const toast = new bootstrap.Toast(toastEl, { delay: 3000 });
    toast.show();
  });
});

function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast align-items-center text-white bg-${type} border-0 position-fixed bottom-0 end-0 m-4`;
  toast.style.zIndex = "1055";
  toast.setAttribute("role", "alert");
  toast.innerHTML = `
    <div class="d-flex">
      <div class="toast-body">${message}</div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>
  `;
  document.body.appendChild(toast);
  new bootstrap.Toast(toast, { delay: 3000 }).show();
}
