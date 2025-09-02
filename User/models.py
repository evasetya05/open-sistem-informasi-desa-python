from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class SystemUser(AbstractUser):
    hiring_manager = 'HR'
    interviewee = 'I'
    team_lead = 'TL'
    position = [
        (hiring_manager, 'Human Resource'),
        (interviewee, 'Interviewee'),
        (team_lead, 'Team Lead'),
    ]
    user_position = models.CharField(
        max_length=2,
        choices=position,
        default=team_lead,
    )

