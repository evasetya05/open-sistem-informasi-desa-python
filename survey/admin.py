from django.contrib import admin
from .models import Survey, Question, Response, Answer

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "is_active", "created_by", "created_at")
    list_filter = ("year", "is_active")
    inlines = [QuestionInline]

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ("id", "survey", "respondent", "status", "submitted_at")
    list_filter = ("status", "survey__year")

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("response", "question", "answer_text")
