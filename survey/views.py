from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseForbidden
from django.urls import reverse
from django.db import transaction

from .models import Survey, Question, Response, Answer
from .forms import SurveyForm, QuestionForm, build_response_form


def _is_staff_desa(user):
    return getattr(user, "user_position", None) in ["SD", "ST"]


@login_required
def survey_manage_list(request):
    """
    STAFF DESA: daftar survey (buat baru, edit, aktif/nonaktif)
    RT/RW/Warga: lihat daftar survey aktif (untuk diisi)
    """
    if _is_staff_desa(request.user):
        surveys = Survey.objects.all().order_by("-year", "-created_at")
        return render(request, "survey/manage_list.html", {"surveys": surveys})
    else:
        surveys = Survey.objects.filter(is_active=True).order_by("-year", "-created_at")
        return render(request, "survey/available_list.html", {"surveys": surveys})


@login_required
def survey_create(request):
    if not _is_staff_desa(request.user):
        return HttpResponseForbidden("Hanya Staff Desa yang bisa membuat survey.")
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect("survey_edit", survey_id=obj.id)
    else:
        form = SurveyForm()
    return render(request, "survey/survey_form.html", {"form": form, "title": "Buat Survey"})


@login_required
def survey_edit(request, survey_id):
    if not _is_staff_desa(request.user):
        return HttpResponseForbidden("Hanya Staff Desa yang bisa mengedit survey.")

    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == "POST":
        form = SurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect("survey_edit", survey_id=survey.id)
    else:
        form = SurveyForm(instance=survey)

    questions = survey.questions.all()
    return render(request, "survey/survey_edit.html", {
        "survey": survey,
        "form": form,
        "questions": questions,
    })


@login_required
def question_create(request, survey_id):
    if not _is_staff_desa(request.user):
        return HttpResponseForbidden("Hanya Staff Desa yang bisa menambah pertanyaan.")
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            q = form.save(commit=False)
            q.survey = survey
            q.save()
            return redirect("survey_edit", survey_id=survey.id)
    else:
        form = QuestionForm()
    return render(request, "survey/question_form.html", {"form": form, "survey": survey, "title": "Tambah Pertanyaan"})


@login_required
def question_edit(request, survey_id, question_id):
    if not _is_staff_desa(request.user):
        return HttpResponseForbidden("Hanya Staff Desa yang bisa mengedit pertanyaan.")
    survey = get_object_or_404(Survey, id=survey_id)
    question = get_object_or_404(Question, id=question_id, survey=survey)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect("survey_edit", survey_id=survey.id)
    else:
        form = QuestionForm(instance=question)
    return render(request, "survey/question_form.html", {"form": form, "survey": survey, "title": "Edit Pertanyaan"})


@login_required
def response_fill(request, survey_id):
    """
    RT/Warga mengisi survey aktif.
    """
    survey = get_object_or_404(Survey, id=survey_id, is_active=True)
    # Cari response milik user (boleh 1 per survey)
    response, _ = Response.objects.get_or_create(survey=survey, respondent=request.user)

    FormClass = build_response_form(survey=survey, instance=response)
    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            save_as = form.cleaned_data.get("save_as", "draft")
            with transaction.atomic():
                # Simpan tiap jawaban
                for q in survey.questions.all():
                    key = f"q_{q.id}"
                    val = form.cleaned_data.get(key)
                    if q.question_type == Question.MULTI and isinstance(val, list):
                        val = ", ".join(val)
                    Answer.objects.update_or_create(
                        response=response,
                        question=q,
                        defaults={"answer_text": str(val) if val is not None else ""},
                    )
                # Update status
                response.status = Response.SUBMITTED if save_as == "submit" else Response.DRAFT
                response.save()
            return redirect("my_responses")
    else:
        form = FormClass()

    return render(request, "survey/response_fill.html", {
        "survey": survey,
        "form": form,
        "response": response,
    })


@login_required
def my_responses(request):
    """
    RT/Warga melihat semua response miliknya.
    """
    responses = Response.objects.filter(respondent=request.user).select_related("survey").order_by("-submitted_at")
    return render(request, "survey/response_my_list.html", {"responses": responses})


@login_required
def rw_review_list(request):
    """
    RW melihat response milik RT di bawahnya yang status SUBMITTED (siap review RW).
    Syarat: user_position == "RW", dan filter berdasarkan parent_rw.
    """
    if getattr(request.user, "user_position", None) != "RW":
        return HttpResponseForbidden("Hanya RW yang bisa mengakses halaman ini.")

    # Ambil semua RT di bawah RW ini
    rt_users = getattr(request.user, "rt_users", None).all() if hasattr(request.user, "rt_users") else []

    responses = Response.objects.filter(
        respondent__in=rt_users,
        status__in=[Response.SUBMITTED, Response.DRAFT]  # bisa lihat draft juga kalau mau
    ).select_related("survey", "respondent").order_by("-submitted_at")

    return render(request, "survey/rw_review_list.html", {"responses": responses})


@login_required
def rw_approve(request, response_id):
    """
    RW approve -> status jadi REVIEW_RW
    """
    if getattr(request.user, "user_position", None) != "RW":
        return HttpResponseForbidden("Hanya RW yang bisa approve.")

    resp = get_object_or_404(Response, id=response_id)
    # Pastikan responden RT berada di bawah RW ini
    if getattr(resp.respondent, "parent_rw_id", None) != request.user.id:
        return HttpResponseForbidden("Tidak berwenang menyetujui data ini.")

    resp.status = Response.REVIEW_RW
    resp.save()
    return redirect("rw_review_list")


@login_required
def staff_review_list(request):
    """
    Staff Desa melihat response yang sudah disetujui RW (REVIEW_RW).
    """
    if not _is_staff_desa(request.user):
        return HttpResponseForbidden("Hanya Staff Desa yang bisa mengakses halaman ini.")

    responses = Response.objects.filter(
        status=Response.REVIEW_RW
    ).select_related("survey", "respondent").order_by("-submitted_at")

    return render(request, "survey/staff_review_list.html", {"responses": responses})


@login_required
def staff_approve(request, response_id):
    """
    Staff Desa approve final -> status APPROVED_STAFF
    """
    if not _is_staff_desa(request.user):
        return HttpResponseForbidden("Hanya Staff Desa yang bisa approve.")

    resp = get_object_or_404(Response, id=response_id)
    resp.status = Response.APPROVED_STAFF
    resp.save()
    return redirect("staff_review_list")
