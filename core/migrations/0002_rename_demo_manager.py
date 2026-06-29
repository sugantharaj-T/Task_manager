from django.conf import settings
from django.db import migrations


def rename_demo_manager(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL.split(".")[0], settings.AUTH_USER_MODEL.split(".")[1])
    Profile = apps.get_model("core", "Profile")

    manager = User.objects.filter(username="manager").first()
    if manager:
        manager.first_name = "Suganth"
        manager.last_name = "Manager"
        if not manager.email:
            manager.email = "manager@example.com"
        manager.save(update_fields=["first_name", "last_name", "email"])
        Profile.objects.update_or_create(
            user=manager,
            defaults={"full_name": "Suganth Manager", "role": "manager", "designation": "Delivery Lead", "department": "Product"},
        )

    Profile.objects.filter(full_name="Priya Manager").update(full_name="Suganth Manager")


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(rename_demo_manager, migrations.RunPython.noop),
    ]
