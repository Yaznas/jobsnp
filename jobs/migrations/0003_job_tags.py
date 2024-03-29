# Generated by Django 4.1.4 on 2023-01-23 06:40

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ("taggit", "0005_auto_20220424_2025"),
        ("jobs", "0002_job_company_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
