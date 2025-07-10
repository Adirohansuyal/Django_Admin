from django import forms
from .models import PersonalInfo, MarksEntry, AdminUser, StudentInfo
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

class StudentInfoForm(forms.ModelForm):
    class Meta:
        model = StudentInfo
        fields = [
            'name', 'age', 'address', 'high_school_math', 'high_school_science',
            'high_school_english', 'high_school_hindi', 'plus_two_physics',
            'plus_two_chemistry', 'plus_two_math'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }