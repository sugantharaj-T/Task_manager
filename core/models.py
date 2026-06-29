from django.conf import settings
from django.db import models


class Profile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("manager", "Project Manager"),
        ("member", "Team Member"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=120)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    designation = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=40, blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return self.full_name or self.user.username


class Project(models.Model):
    STATUS_CHOICES = [
        ("planning", "Planning"),
        ("active", "Active"),
        ("on_hold", "On Hold"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=160)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planning")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_projects")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="projects", blank=True)

    def __str__(self):
        return self.name

    @property
    def completion(self):
        total = self.tasks.count()
        if total == 0:
            return 0
        return round(self.tasks.filter(status="done").count() / total * 100)


class Sprint(models.Model):
    name = models.CharField(max_length=140)
    goal = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="sprints")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("review", "Review"),
        ("done", "Done"),
        ("blocked", "Blocked"),
    ]

    title = models.CharField(max_length=180)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    sprint = models.ForeignKey(Sprint, on_delete=models.SET_NULL, related_name="tasks", null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="assigned_tasks", null=True, blank=True)
    reviewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="review_tasks", blank=True)
    dependency = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=1, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="attachments/")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ActivityLog(models.Model):
    action = models.CharField(max_length=160)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activity", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
