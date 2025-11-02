from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


# ====================================
# LOGIN FORM
# ====================================
class UserLoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']


# ====================================
# SIGNUP FORM (tanpa first/last name)
# ====================================
class UserSignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered!')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken!')
        return username

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match!')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hapus help_text bawaan Django
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ====================================
# UPDATE FORM (tanpa first/last name)
# ====================================
class UserUpdateForm(forms.ModelForm):
    password1 = forms.CharField(label="New Password", widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'user_position']  # ✅ first_name & last_name dihapus

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('instance')
        # Sembunyikan user_position kalau bukan HR
        if user and hasattr(user, 'user_position') and user.user_position != 'HR':
            self.fields['user_position'].widget = forms.HiddenInput()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 or password2:
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
