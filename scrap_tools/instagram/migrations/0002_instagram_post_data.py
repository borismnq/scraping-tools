# Generated by Django 3.1 on 2020-08-27 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagram',
            name='post_data',
            field=models.TextField(default=''),
        ),
    ]
