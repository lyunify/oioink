// ----------------------------------------------------------------------------

// functions
// use form for submit
const fileuploadForm = document.getElementById("directory-upload-form");
fileuploadForm.addEventListener("submit", function () {
    const form = $(this).closest("form");
    const status_message = form.attr("status_message");
    showAlert();
    showProgress();
});

function showAlert() {
    // Get the alert msg element
    const alertMsg = document.getElementById("alert-msg");
    alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>Uploading files and creating vector DB in progress</div>";
    // Remove message after 60 seconds
    setTimeout(() => alertMsg.remove(), 60000);
}

function showProgress() {
    // Get the progress bar element
    const progressBar = document.getElementById("id_progress_bar");
    // Set the initial width of the progress bar to 0
    progressBar.style.width = "0";
    // Define the total duration of the progress in milliseconds (e.g., 5000ms = 5 seconds)
    var totalDuration = 60000;
    // Update the progress bar at a specific interval (e.g., every 100ms)
    var updateInterval = 100;
    // Calculate the width increment for each interval
    var increment = (updateInterval / totalDuration) * 100;
    // Start the progress
    var currentWidth = 0;
    var interval = setInterval(function () {
        currentWidth += increment;
        progressBar.style.width = currentWidth + "%";
        // Check if the progress is complete
        if (currentWidth >= 100) {
            clearInterval(interval);
            // alert("Progress completed!");
        }
    }, updateInterval);
}
