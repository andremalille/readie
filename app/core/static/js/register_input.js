
const passwordInput = document.getElementById('id_password');
const confirmPasswordInput = document.getElementById('id_confirm_password');
const confirmPasswordContainer = document.getElementById('confirm-password-container');
const passwordMatchError = document.getElementById('password-match-error');
const signupButton = document.getElementById('signup-button');

function checkPasswordsMatch() {
    if (passwordInput.value && confirmPasswordInput.value) {
        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordMatchError.style.display = 'block';
            signupButton.disabled = true;
            signupButton.classList.add('button-disabled');
            return false;
        } else {
            passwordMatchError.style.display = 'none';
            signupButton.disabled = false;
            signupButton.classList.remove('button-disabled');
            return true;
        }
    }
    return true;
}

document.addEventListener('DOMContentLoaded', function () {

    const hasErrors = document.querySelectorAll('.errorlist').length > 0;
    const hasConfirmPasswordErrors = document.querySelector('#confirm-password-container .errorlist') !== null;
    const hasNonFieldErrors = document.querySelector('form > .error') !== null;

    if (passwordInput.value) {
        confirmPasswordContainer.classList.add('show');
        checkPasswordsMatch();
    } else {
        confirmPasswordContainer.classList.remove('show');

        if (hasConfirmPasswordErrors) {
            const errorElements = document.querySelectorAll('#confirm-password-container .errorlist');
            const formElement = document.querySelector('.form');

            let formLevelErrorContainer = document.getElementById('form-level-errors');
            if (!formLevelErrorContainer) {
                formLevelErrorContainer = document.createElement('div');
                formLevelErrorContainer.id = 'form-level-errors';
                formElement.insertBefore(formLevelErrorContainer, signupButton);
            }

            errorElements.forEach(function (errorElement) {
                const clonedError = errorElement.cloneNode(true);
                clonedError.classList.add('form-level-error');
                formLevelErrorContainer.appendChild(clonedError);

                errorElement.style.display = 'none';
            });
        }
    }
});

passwordInput.addEventListener('input', function () {
    if (this.value.length > 0) {
        confirmPasswordContainer.classList.add('show');
        checkPasswordsMatch();
    } else {
        confirmPasswordContainer.classList.remove('show');
        passwordMatchError.style.display = 'none';
        signupButton.disabled = false;
        signupButton.classList.remove('button-disabled');
    }
});

confirmPasswordInput.addEventListener('input', function () {
    checkPasswordsMatch();
});

document.querySelector('.form').addEventListener('submit', function (event) {
    if (passwordInput.value && confirmPasswordInput.value) {
        if (!checkPasswordsMatch()) {
            event.preventDefault();
        }
    }
});
