from django import forms
from .models import Survey, Question, Response, Answer

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["name", "description", "year", "is_active"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "question_type", "choices", "order"]
        help_texts = {
            "choices": "Pisahkan pilihan dengan koma (hanya untuk Single/Multi Choice)."
        }



def build_response_form(survey: Survey, instance: Response | None = None):
    """
    Membangun form dinamis berdasarkan daftar pertanyaan di Survey.
    """
    class _ResponseForm(forms.Form):
        pass

    # Prefill jawaban kalau ada response lama
    prev = {}
    if instance:
        prev = {a.question_id: a.answer_text for a in instance.answers.all()}

    # Buat field sesuai tipe pertanyaan
    for q in survey.questions.all():
        field_name = f"q_{q.id}"
        initial = prev.get(q.id, "")

        if q.question_type == Question.TEXT:
            field = forms.CharField(label=q.text, required=False, initial=initial)
        elif q.question_type == Question.NUMBER:
            field = forms.DecimalField(label=q.text, required=False, initial=initial)
        elif q.question_type == Question.CHOICE:
            choices = [(c, c) for c in q.get_choices()]
            field = forms.ChoiceField(label=q.text, choices=choices, required=False, initial=initial)
        elif q.question_type == Question.MULTI:
            choices = [(c, c) for c in q.get_choices()]
            initial_list = [s.strip() for s in str(initial).split(",")] if initial else []
            field = forms.MultipleChoiceField(
                label=q.text,
                choices=choices,
                required=False,
                initial=initial_list
            )
        else:
            field = forms.CharField(label=q.text, required=False, initial=initial)

        # ✅ Gunakan base_fields supaya terdaftar di form
        _ResponseForm.base_fields[field_name] = field

    # Tambahkan hidden field untuk status simpan
    _ResponseForm.base_fields["save_as"] = forms.CharField(
        widget=forms.HiddenInput, initial="draft", required=False
    )

    return _ResponseForm

