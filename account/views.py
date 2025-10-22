from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import redirect, render
from django.views.generic import FormView, ListView, UpdateView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserSignupForm, UserUpdateForm
from django.contrib.auth.decorators import login_required

User = get_user_model()


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('dashboard:index')

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])
        if user:
            login(self.request, user)
            return redirect('dashboard:index')
        else:
            form.add_error('username', "Error On Credentials")
            return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().get(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('dashboard:index')


class UserSignupView(FormView):
    form_class = UserSignupForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        new_user = User(
            email=cleaned_data['email'],
            username=cleaned_data['username'],
        )
        new_user.set_password(cleaned_data['password1'])
        new_user.save()

        messages.success(self.request, 'Registration Success. Please Login.')
        return redirect('user:login')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:index')
        return super().get(request, *args, **kwargs)


class ListUserView(ListView):
    model = User
    template_name = 'account/list-user.html'
    queryset = User.objects.all()
    context_object_name = 'user_list'

    def get(self, request, *args, **kwargs):
        if not hasattr(request.user, 'user_position') or request.user.user_position != 'HR':
            return redirect(reverse_lazy('dashboard:index'))
        return super().get(request, *args, **kwargs)


class EditUserView(UpdateView):
    model = User
    template_name = 'account/edit-user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('user:list')

@login_required
def user_profile(request, user_id=None):
    """
    View untuk menampilkan dan mengupdate profil pengguna.
    Hanya HR yang dapat melihat profil pengguna lain.
    """
    # Jika user_id tidak diberikan, anggap itu adalah profil pengguna yang sedang login
    if user_id is None:
        user = request.user
    else:
        # Hanya HR yang bisa melihat profil pengguna lain
        if not hasattr(request.user, 'user_position') or request.user.user_position != 'HR':
            return redirect('dashboard:index')  # Redirect jika bukan HR
        user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
        else:
            messages.error(request, 'Terjadi kesalahan saat memperbarui profil Anda.')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'account/update_user_profile.html', {'form': form, 'user': user})
