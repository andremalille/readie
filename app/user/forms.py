from django import forms
from core.models import User
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'confirm_password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return cleaned_data


class UserChangeInfoForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change password",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'old_password', 'new_password', 'confirm_new_password')

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")

        if new_password or old_password or confirm_new_password:
            if old_password and not self.instance.check_password(old_password):
                self.add_error(
                    'old_password',
                    "Your old password was entered incorrectly."
                )

            if new_password != confirm_new_password:
                self.add_error(
                    'confirm_new_password',
                    "New passwords don't match."
                )

            if new_password and not old_password:
                self.add_error(
                    'old_password',
                    "Please enter your old password to set a new one."
                )

        return cleaned_data
