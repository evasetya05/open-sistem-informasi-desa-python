from django.shortcuts import render
from django.contrib.auth import get_user_model

from Job.models import Jobs, Application

User = get_user_model()


def index(request):
    # current_user = User.objects.get(id=request.)
    # print(current_user.position)
    jobs = Jobs.objects

    if request.user.is_authenticated:
        current_user = request.user
        if current_user.user_position == 'HR':
            applications = Application.objects.filter(job_id__in=jobs.all())

            return render(request, 'hr-dashboard.html')
            # opsi lama return render(request, 'Dashboard/hr-dashboard.html', context={'jobs': jobs.all(), 'applications':applications})

        elif current_user.user_position == 'TL':
            jobs = Jobs.objects.filter(team_lead=request.user)
            applications = Application.objects.filter(job_id__in=jobs)
            print(applications)
            return render(request, 'tl-dashboard.html',
                          context={'jobs': jobs.all(), 'applications': applications})

        elif current_user.user_position == 'I':
            applied_application = Application.objects.filter(applicant_id=request.user.id)
            applied_jobs = []
            for application in applied_application:
                applied_jobs.append(application.job.id)
            jobs = jobs.exclude(id__in=applied_jobs)
            print(applied_application)
            print(jobs)
            # print(applied_application)
            return render(request, 'i-dashboard.html',
                          context={'jobs': jobs, 'applied_jobs': applied_application})

    return render(request, 'i-dashboard.html', context={'jobs': jobs.all()})


def base(request):
    return render(request, 'partials/base.html')

