document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("add-job-form").addEventListener("submit", function(event) {
        event.preventDefault();
        const form = this;
        const formData = new FormData(form); // gather data from form

        fetch(form.action, { // Sends a POST request to the form's action URL
            method: "POST",
            body: formData
        })
        .then(response => response.json()) // waits for and parses response to text as JSON
        .then(data => { 
            if (data.duplicate) {
                const userConfirmed = confirm("You have already added a similar job recently. Are you sure you want to add it?");
                
                if (userConfirmed) {
                    document.getElementById("force_submit").value ="true";
                    form.onsubmit();
                }
            } else {
                form.submit();
            }         
        })
        .catch(error => {
            console.error("Error: ", error);
            alert("An error has occurred. Please try again!");
        });
    });
});