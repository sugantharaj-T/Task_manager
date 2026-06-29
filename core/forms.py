from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Project, Task


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=120)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["full_name", "email", "username", "password1", "password2"]


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email or username")

    def clean(self):
        login_value = self.cleaned_data.get("username")
        if login_value and "@" in login_value:
            matched_user = User.objects.filter(email__iexact=login_value).first()
            if matched_user:
                self.cleaned_data["username"] = matched_user.username
        return super().clean()


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.order_by("first_name", "last_name", "username")
        self.fields["members"].queryset = users
        self.fields["members"].help_text = "Hold Ctrl to select more than one team member."
        self.fields["members"].label_from_instance = self._user_label

    @staticmethod
    def _user_label(user):
        return user.get_full_name() or user.username

    class Meta:
        model = Project
        fields = ["name", "description", "start_date", "end_date", "status", "members"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "members": forms.SelectMultiple(attrs={"size": 5}),
        }


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = User.objects.order_by("first_name", "last_name", "username")
        self.fields["assignee"].queryset = users
        self.fields["reviewers"].queryset = users
        self.fields["assignee"].label_from_instance = self._user_label
        self.fields["reviewers"].label_from_instance = self._user_label
        self.fields["reviewers"].help_text = "Hold Ctrl to select more than one reviewer."

    @staticmethod
    def _user_label(user):
        return user.get_full_name() or user.username

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "project",
            "sprint",
            "priority",
            "status",
            "assignee",
            "reviewers",
            "dependency",
            "start_date",
            "due_date",
            "estimated_hours",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "reviewers": forms.SelectMultiple(attrs={"size": 4}),
        }
