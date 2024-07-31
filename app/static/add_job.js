document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("add-job-form").addEventListener("submit", function(event) {
        event.preventDefault();
        const form = this;
        const formData = new FormData(form); // gather data from form
    });
});