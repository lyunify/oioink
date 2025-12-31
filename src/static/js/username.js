// ----------------------------------------------------------------------------
// validate username
$(document).ready(function () {
    // catch the form's submit event
    $('#id_username').keyup(function () {
        // clear any error message
        $('#id_username_error').remove();
        // check username
        const username = $(this).val();
        if (username.length < 5 || username.length > 30) {
            $('#id_username').removeClass('is-valid').addClass('is-invalid');
            $('#id_username').after('<div class="invalid-feedback d-block" id="id_username_error">Username must be between 5 and 30 characters!</div>');
            // to prevent form from submitting and page reload
            return false;
        }
        // make AJAX call to validate username
        const form = $(this).closest("form");
        $.ajax({
            data: $(this).serialize(), // get the form data
            url: form.attr("validate-username"),
            // on success
            success: function (response) {
                if (response.is_taken == true) {
                    $('#id_username').removeClass('is-valid').addClass('is-invalid');
                    $('#id_username').after('<div class="invalid-feedback d-block" id="id_username_error">This username is not available!</div>');
                }
                else {
                    $('#id_username').removeClass('is-invalid').addClass('is-valid');
                    $('#id_username_error').remove();
                }
            },
            // on error
            error: function (response) {
                // alert the error if any error occured
                console.log(response.responseJSON.errors);
            }
        });
        // to prevent form from submitting and page reload
        return false;
    });
});
