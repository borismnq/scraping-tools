# Generated by Django 3.1 on 2020-08-27 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("elpais", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="elpais",
            name="text",
            field=models.TextField(default=""),
        ),
    ]
