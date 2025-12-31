// ----------------------------------------------------------------------------

// functions
// use form for submit
const chatForm = document.getElementById("chat-form");
chatForm.addEventListener("submit", function () {
    const form = $(this).closest("form");
    const status_message = form.attr("status_message");
    showAlert();
    showSpinner();
});

function showAlert() {
    // Get the alert msg element
    const alertMsg = document.getElementById("alert-msg");
    alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>Uploading file and creating vector DB in progress</div>";
    // Remove message after 60 seconds
    setTimeout(() => alertMsg.remove(), 60000);
}

function showSpinner() {
    // Get the progress bar element
    const spinner = document.getElementById("id_spinner");
}
