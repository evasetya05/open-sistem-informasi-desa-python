from django.urls import path
from . import views

urlpatterns = [
    # Staff Desa: kelola survey
    path("", views.survey_manage_list, name="survey_home"),  # Staff: manage; RT/RW/Warga: daftar survey aktif
    path("create/", views.survey_create, name="survey_create"),
    path("<int:survey_id>/edit/", views.survey_edit, name="survey_edit"),
    path("<int:survey_id>/questions/add/", views.question_create, name="question_create"),
    path("<int:survey_id>/questions/<int:question_id>/edit/", views.question_edit, name="question_edit"),

    # Mengisi survey
    path("<int:survey_id>/fill/", views.response_fill, name="response_fill"),
    path("my-responses/", views.my_responses, name="my_responses"),

    # RW review & approval
    path("rw/review/", views.rw_review_list, name="rw_review_list"),
    path("rw/approve/<int:response_id>/", views.rw_approve, name="rw_approve"),

    # Staff final approval
    path("staff/review/", views.staff_review_list, name="staff_review_list"),
    path("staff/approve/<int:response_id>/", views.staff_approve, name="staff_approve"),




    path("list/", views.survey_list, name="survey_list"),
    path("rw/review/<int:survey_id>/", views.survey_review_rw, name="survey_review_rw"),
    path("staff/approve/<int:survey_id>/", views.survey_approve_staff, name="survey_approve_staff"),
]

