from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SystemUser

def is_kepala_desa(user):
    return user.is_authenticated and user.user_position == SystemUser.kepala_desa

@login_required
@user_passes_test(is_kepala_desa)
def manage_users(request):
    users = SystemUser.objects.exclude(pk=request.user.pk)  # semua user kecuali kepala desa
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_position = request.POST.get('user_position')
        parent_rw_id = request.POST.get('parent_rw')

        try:
            target_user = SystemUser.objects.get(pk=user_id)
            target_user.user_position = new_position
            target_user.parent_rw_id = parent_rw_id or None
            target_user.save()
            messages.success(request, f"Posisi {target_user.username} berhasil diubah menjadi {target_user.get_user_position_display()}.")
        except SystemUser.DoesNotExist:
            messages.error(request, "User tidak ditemukan.")

        return redirect('manage_users')

    context = {
        'users': users,
        'rws': SystemUser.objects.filter(user_position=SystemUser.rw)
    }
    return render(request, 'user/manage_users.html', context)
