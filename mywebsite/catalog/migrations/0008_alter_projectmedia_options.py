# Generated by Django 5.2.3 on 2025-06-18 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0007_rename_projectimage_projectmedia"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="projectmedia",
            options={"ordering": ["order"]},
        ),
    ]
