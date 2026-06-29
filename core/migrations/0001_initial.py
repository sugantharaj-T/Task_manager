import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("description", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("status", models.CharField(choices=[("planning", "Planning"), ("active", "Active"), ("on_hold", "On Hold"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="planning", max_length=20)),
                ("manager", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="managed_projects", to=settings.AUTH_USER_MODEL)),
                ("members", models.ManyToManyField(blank=True, related_name="projects", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=120)),
                ("role", models.CharField(choices=[("admin", "Administrator"), ("manager", "Project Manager"), ("member", "Team Member")], default="member", max_length=20)),
                ("designation", models.CharField(blank=True, max_length=100)),
                ("department", models.CharField(blank=True, max_length=100)),
                ("contact", models.CharField(blank=True, max_length=40)),
                ("photo", models.ImageField(blank=True, null=True, upload_to="profiles/")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Sprint",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=140)),
                ("goal", models.TextField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sprints", to="core.project")),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("description", models.TextField()),
                ("priority", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical")], default="medium", max_length=20)),
                ("status", models.CharField(choices=[("todo", "To Do"), ("in_progress", "In Progress"), ("review", "Review"), ("done", "Done"), ("blocked", "Blocked")], default="todo", max_length=20)),
                ("start_date", models.DateField()),
                ("due_date", models.DateField()),
                ("estimated_hours", models.DecimalField(decimal_places=1, default=1, max_digits=5)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("assignee", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="assigned_tasks", to=settings.AUTH_USER_MODEL)),
                ("dependency", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.task")),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="core.project")),
                ("reviewers", models.ManyToManyField(blank=True, related_name="review_tasks", to=settings.AUTH_USER_MODEL)),
                ("sprint", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tasks", to="core.sprint")),
            ],
        ),
        migrations.CreateModel(
            name="Attachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.FileField(upload_to="attachments/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attachments", to="core.task")),
                ("uploaded_by", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("body", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="core.task")),
            ],
        ),
        migrations.CreateModel(
            name="ActivityLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("action", models.CharField(max_length=160)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("task", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="activity", to="core.task")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
