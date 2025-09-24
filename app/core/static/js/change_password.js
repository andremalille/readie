
const passwordInput = document.getElementById('id_new_password');
const confirmPasswordInput = document.getElementById('id_confirm_new_password');
const confirmPasswordContainer = document.getElementById('confirm-new-password-container');
const passwordMatchError = document.getElementById('password-match-error');

document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.querySelector('.change-info-button');
    submitButton.classList.remove('disabled');
});

passwordInput.addEventListener('input', function () {
    const submitButton = document.querySelector('.change-info-button');

    if (this.value.length > 0) {
        confirmPasswordContainer.classList.add('show');
    } else {
        confirmPasswordContainer.classList.remove('show');
        passwordMatchError.classList.add('hidden');
        submitButton.classList.remove('disabled');
    }

    if (this.value.length > 0 && confirmPasswordInput.value.length > 0) {
        checkPasswordsMatch();
    } else if (this.value.length === 0) {
        submitButton.classList.remove('disabled');
    }
});

confirmPasswordInput.addEventListener('input', function () {
    const submitButton = document.querySelector('.change-info-button');

    if (passwordInput.value.length > 0 && this.value.length > 0) {
        checkPasswordsMatch();
    } else {
        passwordMatchError.classList.add('hidden');
        if (passwordInput.value.length === 0) {
            submitButton.classList.remove('disabled');
        }
    }
});

function checkPasswordsMatch() {
    const submitButton = document.querySelector('.change-info-button');

    if (passwordInput.value !== confirmPasswordInput.value) {
        passwordMatchError.classList.remove('hidden');
        submitButton.classList.add('disabled');
    } else {
        passwordMatchError.classList.add('hidden');
        submitButton.classList.remove('disabled');
    }
}
