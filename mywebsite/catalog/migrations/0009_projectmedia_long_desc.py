# Generated by Django 5.2.3 on 2025-06-18 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0008_alter_projectmedia_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="projectmedia",
            name="long_desc",
            field=models.TextField(
                help_text="Enter the media description", max_length=5000, null=True
            ),
        ),
    ]
