from django.db import models
from django.contrib.auth.models import AbstractUser

class SystemUser(AbstractUser):
    kepala_desa = 'KD'
    sekretaris_desa = 'SD'
    staff_desa = 'ST'
    rw = 'RW'
    rt = 'RT'
    warga = 'WG'

    POSITION_CHOICES = [
        (kepala_desa, 'Kepala Desa'),
        (sekretaris_desa, 'Sekretaris Desa'),
        (staff_desa, 'Staff Desa'),
        (rw, 'RW'),
        (rt, 'RT'),
        (warga, 'Warga'),
    ]

    user_position = models.CharField(
        max_length=2,
        choices=POSITION_CHOICES,
        default=warga,
    )

    # Relasi RT ke RW
    parent_rw = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rt_users",
        limit_choices_to={"user_position": rw},
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_position_display()})"
