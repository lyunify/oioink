// ----------------------------------------------------------------------------
// check file size for submit
const timeOut = 10000; // 10 secs
const fileSize = 20480; // 20 KB
const imageFile = document.getElementById("id_image_file");
const imageError = document.getElementById("id_image_error");
imageFile.addEventListener("change", () => {
    if (imageFile.files[0].size > fileSize) {
        imageFile.classList.remove('is-valid');
        imageFile.classList.add('is-invalid');
        imageError.innerHTML = "<div class='alert alert-danger d-inline-flex' role='alert'>File exceeded 20KB!</div>";
        setTimeout(() => imageError.remove(), timeOut);
        imageFile.value = '';
        imageFile.focus();
    } else {
        imageFile.classList.remove('is-invalid');
        imageFile.classList.add('is-valid');
    }
});
