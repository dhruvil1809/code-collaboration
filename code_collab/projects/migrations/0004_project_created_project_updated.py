# Generated by Django 5.0.7 on 2024-08-15 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_file_filename_file_name_fileversion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 8, 15, 9, 51, 1, 992740, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
