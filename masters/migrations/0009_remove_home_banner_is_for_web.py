# Generated by Django 5.1.4 on 2025-07-24 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0008_remove_home_banner_description_home_banner_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='home_banner',
            name='is_for_web',
        ),
    ]
