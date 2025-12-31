// ----------------------------------------------------------------------------
// locations
const alertMsg = document.getElementById("alert-msg");

// functions
// use form for submit
const contactForm = document.getElementById("contact-form");
contactForm.addEventListener("submit", function () {
    const form = $(this).closest("form");
    const status_message = form.attr("status_message");
    if (status_message) {
        alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>Message sent successfully!</div>";
    } else {
        alertMsg.innerHTML = "<div class='alert alert-danger d-inline-flex' role='alert'>Message not sent!</div>";
    }
    // Remove error after 10 seconds
    setTimeout(() => alertMsg.remove(), 20000);
});
