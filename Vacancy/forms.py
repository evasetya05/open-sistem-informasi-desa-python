from django import forms

from Job.models import Jobs, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = ['title', 'required_position']


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cv']
