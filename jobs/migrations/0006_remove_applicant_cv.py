# Generated by Django 4.1.5 on 2023-01-24 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0005_applicant_cv_alter_applicant_job_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="applicant",
            name="cv",
        ),
    ]
