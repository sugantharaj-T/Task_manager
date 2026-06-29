from django.contrib import admin

from .models import ActivityLog, Attachment, Comment, Profile, Project, Sprint, Task

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(ActivityLog)
