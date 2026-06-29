from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("projects/", views.projects, name="projects"),
    path("projects/new/", views.project_create, name="project_create"),
    path("projects/<int:pk>/edit/", views.project_edit, name="project_edit"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/new/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:pk>/status/<str:status>/", views.task_status, name="task_status"),
    path("kanban/", views.kanban, name="kanban"),
    path("calendar/", views.calendar, name="calendar"),
    path("reports/", views.reports, name="reports"),
    path("profile/", views.profile, name="profile"),
]
