# Generated by Django 4.1.5 on 2023-01-29 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("createresume", "0004_alter_resume_education_alter_resume_projects_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="resume",
            name="location",
            field=models.CharField(max_length=200, null=True),
        ),
    ]
