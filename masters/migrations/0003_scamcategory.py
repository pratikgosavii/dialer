# Generated by Django 5.1.4 on 2025-05-30 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0002_faq'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScamCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]
