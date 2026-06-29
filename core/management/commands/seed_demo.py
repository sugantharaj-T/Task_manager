from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import ActivityLog, Profile, Project, Sprint, Task


class Command(BaseCommand):
    help = "Create demo users, projects, sprints and tasks for the TaskFlow frontend."

    def handle(self, *args, **options):
        manager, _ = User.objects.get_or_create(
            username="manager",
            defaults={"email": "manager@example.com", "first_name": "Suganth", "last_name": "Manager"},
        )
        manager.first_name = "Suganth"
        manager.last_name = "Manager"
        manager.email = manager.email or "manager@example.com"
        manager.set_password("manager123")
        manager.save()
        Profile.objects.update_or_create(
            user=manager,
            defaults={"full_name": "Suganth Manager", "role": "manager", "designation": "Delivery Lead", "department": "Product"},
        )

        member, _ = User.objects.get_or_create(
            username="alex",
            defaults={"email": "alex@example.com", "first_name": "Alex", "last_name": "Member"},
        )
        member.set_password("alex123")
        member.save()
        Profile.objects.get_or_create(user=member, defaults={"full_name": "Alex Member", "role": "member", "designation": "Frontend Developer", "department": "Engineering"})

        project, _ = Project.objects.get_or_create(
            name="Task Manager Platform",
            defaults={
                "description": "A Jira-style project and task management system with dashboards, kanban, calendar and reports.",
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=45),
                "status": "active",
                "manager": manager,
            },
        )
        project.members.add(manager, member)

        sprint, _ = Sprint.objects.get_or_create(
            name="Sprint 1",
            project=project,
            defaults={"goal": "Launch the core task workflow.", "start_date": date.today(), "end_date": date.today() + timedelta(days=14)},
        )

        seeds = [
            ("Design authentication screens", "high", "done", 2),
            ("Build project dashboard", "critical", "in_progress", 5),
            ("Create kanban workflow", "high", "review", 8),
            ("Add comments and activity log", "medium", "todo", 12),
            ("Prepare reporting charts", "medium", "blocked", 16),
        ]
        for title, priority, status, days in seeds:
            task, _ = Task.objects.get_or_create(
                title=title,
                project=project,
                defaults={
                    "description": f"Demo work item for {title.lower()}.",
                    "sprint": sprint,
                    "priority": priority,
                    "status": status,
                    "assignee": member,
                    "start_date": date.today(),
                    "due_date": date.today() + timedelta(days=days),
                    "estimated_hours": 6,
                },
            )
            ActivityLog.objects.get_or_create(action=f"Demo task seeded: {task.title}", task=task, user=manager)

        self.stdout.write(self.style.SUCCESS("Demo data ready. Login as manager / manager123."))
