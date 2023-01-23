from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(
            name="Makrod",
            email="makrod@gmail.com",
            is_staff=True,
            is_superuser=True,
            phone="7016523631",
            gender="Male",
        )
        user.set_password("Makrod")
        user.save()

    dependencies = [
        
    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
