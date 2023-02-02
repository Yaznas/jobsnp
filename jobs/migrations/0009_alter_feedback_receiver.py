# Generated by Django 4.1.5 on 2023-01-31 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jobs", "0008_rename_recipient_feedback_receiver"),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="receiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="receiver",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]