from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Survey(models.Model):
    name = models.CharField(max_length=255)  # Contoh: "Survey Sosial Ekonomi 2025"
    description = models.TextField(blank=True)
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)  # Staff bisa stop/lanjut
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_surveys")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "AKTIF" if self.is_active else "NONAKTIF"
        return f"{self.name} ({self.year}) - {status}"


class Question(models.Model):
    TEXT = "text"
    NUMBER = "number"
    CHOICE = "choice"
    MULTI = "multi"

    QUESTION_TYPES = [
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (CHOICE, "Single Choice"),
        (MULTI, "Multiple Choice"),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=500)  # Isi pertanyaan
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT)
    # Untuk choice/multi: pisahkan dengan koma, contoh: "Ya,Tidak,Tidak Tahu"
    choices = models.TextField(blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def get_choices(self):
        return [c.strip() for c in self.choices.split(",")] if self.choices else []

    def __str__(self):
        return f"[{self.get_question_type_display()}] {self.text}"


class Response(models.Model):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    REVIEW_RW = "review_rw"
    APPROVED_STAFF = "approved_staff"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (SUBMITTED, "Dikirim"),
        (REVIEW_RW, "Disetujui RW"),
        (APPROVED_STAFF, "Disetujui Staff Desa"),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="responses")
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)  # RT/Warga pengisi
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response {self.id} - {self.survey.name} - {self.respondent}"


class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("response", "question")

    def __str__(self):
        return f"{self.question.text}: {self.answer_text}"
