// ----------------------------------------------------------------------------
// locations
const alertMsg = document.getElementById("alert-msg");

// functions
// Use form for submit
const searchForm = document.getElementById("search-form")
searchForm.addEventListener("submit", function () {
    // alert('The target may take 10-15 mins to process and analyze.');
    alertMsg.innerHTML = "<div class='alert alert-success d-inline-flex' role='alert'>The target may take 10-15 mins to process and analyze.</div>";
    // Remove error after 10 seconds
    setTimeout(() => alertMsg.remove(), 20000);
});
