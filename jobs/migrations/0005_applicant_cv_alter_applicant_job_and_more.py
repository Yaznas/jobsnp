# Generated by Django 4.1.5 on 2023-01-24 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0004_bookmarkjob"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicant",
            name="cv",
            field=models.FileField(null=True, upload_to="docs/"),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applicants",
                to="jobs.job",
            ),
        ),
        migrations.AlterField(
            model_name="bookmarkjob",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bookmarks",
                to="jobs.job",
            ),
        ),
    ]
