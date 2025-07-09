from django import forms
from .models import PersonalInfo, MarksEntry, AdminUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .base_form import BaseForm

class PersonalInfoForm(BaseForm):
    class Meta:
        model = PersonalInfo
        fields = ['full_name', 'address', 'date_of_birth']

class MarksEntryForm(BaseForm):
    class Meta:
        model = MarksEntry
        fields = ['subject', 'marks_obtained', 'total_marks']

class AdminSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AdminUser
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class AdminLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'