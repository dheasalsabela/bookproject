# Generated by Django 5.1.3 on 2024-12-13 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_userbookcollection_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='status',
        ),
    ]
