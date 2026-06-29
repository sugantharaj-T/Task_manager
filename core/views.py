from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm, RegisterForm, TaskForm
from .models import ActivityLog, Comment, Profile, Project, Task


def _ensure_profile(user):
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"full_name": user.get_full_name() or user.username, "role": "manager"},
    )
    return profile


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data["full_name"]
            user.first_name = full_name.split(" ")[0]
            user.last_name = " ".join(full_name.split(" ")[1:])
            user.email = form.cleaned_data["email"]
            user.save()
            Profile.objects.create(user=user, full_name=full_name, role="manager")
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "auth/register.html", {"form": form})


@login_required
def dashboard(request):
    _ensure_profile(request.user)
    tasks = Task.objects.select_related("project", "assignee").all()
    projects = Project.objects.prefetch_related("members").all()
    stats = {
        "users": User.objects.count(),
        "active_projects": projects.filter(status="active").count(),
        "completed_projects": projects.filter(status="completed").count(),
        "open_tasks": tasks.exclude(status="done").count(),
        "overdue": tasks.filter(due_date__lt=date.today()).exclude(status="done").count(),
    }
    upcoming = tasks.filter(due_date__gte=date.today()).order_by("due_date")[:6]
    activity = ActivityLog.objects.select_related("task", "user").order_by("-created_at")[:8]
    return render(request, "dashboard.html", {"stats": stats, "projects": projects[:5], "upcoming": upcoming, "activity": activity})


@login_required
def projects(request):
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    projects_qs = Project.objects.prefetch_related("members").annotate(task_count=Count("tasks"))
    if query:
        projects_qs = projects_qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if status:
        projects_qs = projects_qs.filter(status=status)
    return render(request, "projects.html", {"projects": projects_qs, "query": query, "status": status, "statuses": Project.STATUS_CHOICES})


@login_required
def project_create(request):
    form = ProjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        project = form.save(commit=False)
        project.manager = request.user
        project.save()
        form.save_m2m()
        project.members.add(request.user)
        messages.success(request, "Project created.")
        return redirect("projects")
    return render(request, "form_page.html", {"form": form, "title": "Create Project", "button": "Save Project"})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Project updated.")
        return redirect("projects")
    return render(request, "form_page.html", {"form": form, "title": "Edit Project", "button": "Update Project"})


@login_required
def tasks(request):
    tasks_qs = Task.objects.select_related("project", "assignee", "sprint").all()
    query = request.GET.get("q", "")
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    assignee = request.GET.get("assignee", "")
    if query:
        tasks_qs = tasks_qs.filter(Q(title__icontains=query) | Q(project__name__icontains=query) | Q(assignee__username__icontains=query))
    if status:
        tasks_qs = tasks_qs.filter(status=status)
    if priority:
        tasks_qs = tasks_qs.filter(priority=priority)
    if assignee:
        tasks_qs = tasks_qs.filter(assignee_id=assignee)
    users = User.objects.order_by("first_name", "last_name", "username")
    return render(
        request,
        "tasks.html",
        {
            "tasks": tasks_qs.order_by("due_date"),
            "statuses": Task.STATUS_CHOICES,
            "priorities": Task.PRIORITY_CHOICES,
            "users": users,
            "filters": {"q": query, "status": status, "priority": priority, "assignee": assignee},
        },
    )


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        if task.assignee:
            task.project.members.add(task.assignee)
        task.project.members.add(*form.cleaned_data["reviewers"])
        ActivityLog.objects.create(action="Task created", task=task, user=request.user)
        messages.success(request, "Task created.")
        return redirect("tasks")
    return render(request, "form_page.html", {"form": form, "title": "Create Task", "button": "Save Task"})


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        task = form.save()
        if task.assignee:
            task.project.members.add(task.assignee)
        task.project.members.add(*form.cleaned_data["reviewers"])
        ActivityLog.objects.create(action="Task updated", task=task, user=request.user)
        messages.success(request, "Task updated.")
        return redirect("task_detail", pk=task.pk)
    return render(request, "form_page.html", {"form": form, "title": "Edit Task", "button": "Update Task"})


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task.objects.select_related("project", "assignee", "dependency"), pk=pk)
    if request.method == "POST":
        body = request.POST.get("body", "").strip()
        if body:
            Comment.objects.create(task=task, author=request.user, body=body)
            ActivityLog.objects.create(action="Comment added", task=task, user=request.user)
            return redirect("task_detail", pk=task.pk)
    return render(request, "task_detail.html", {"task": task})


@login_required
def task_status(request, pk, status):
    task = get_object_or_404(Task, pk=pk)
    if status in dict(Task.STATUS_CHOICES):
        task.status = status
        task.save(update_fields=["status", "updated_at"])
        ActivityLog.objects.create(action=f"Status updated to {task.get_status_display()}", task=task, user=request.user)
    return redirect(request.META.get("HTTP_REFERER", "kanban"))


@login_required
def kanban(request):
    grouped = {key: Task.objects.select_related("project", "assignee").filter(status=key).order_by("due_date") for key, _ in Task.STATUS_CHOICES}
    return render(request, "kanban.html", {"grouped": grouped, "statuses": Task.STATUS_CHOICES})


@login_required
def calendar(request):
    start = date.today()
    end = start + timedelta(days=30)
    tasks_qs = Task.objects.select_related("project").filter(due_date__range=(start, end)).order_by("due_date")
    return render(request, "calendar.html", {"tasks": tasks_qs, "start": start, "end": end})


@login_required
def reports(request):
    total = Task.objects.count()
    done = Task.objects.filter(status="done").count()
    overdue = Task.objects.filter(due_date__lt=date.today()).exclude(status="done").count()
    completion = round(done / total * 100) if total else 0
    by_status = Task.objects.values("status").annotate(total=Count("id"))
    by_priority = Task.objects.values("priority").annotate(total=Count("id"))
    return render(request, "reports.html", {"total": total, "done": done, "overdue": overdue, "completion": completion, "by_status": by_status, "by_priority": by_priority})


@login_required
def profile(request):
    profile_obj = _ensure_profile(request.user)
    assigned = request.user.assigned_tasks.select_related("project").order_by("due_date")[:8]
    return render(request, "profile.html", {"profile": profile_obj, "assigned": assigned})
