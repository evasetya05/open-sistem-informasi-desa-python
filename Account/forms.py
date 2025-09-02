from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('This email is already registered!')
        return self.cleaned_data['email']

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('This username is already taken!')
        return self.cleaned_data['username']

    def clean(self):
        if self.cleaned_data.get('password1') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match!')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]




class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User  # Ensure this is the correct model you're working with
        fields = ['username','first_name', 'last_name', 'email', 'user_position']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')
        if user and hasattr(user, 'user_position') and user.user_position != 'HR':
            self.fields['user_position'].widget = forms.HiddenInput()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

