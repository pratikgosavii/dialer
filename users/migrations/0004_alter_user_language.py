# Generated by Django 5.1.4 on 2025-06-01 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_mobile_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(blank=True, choices=[('english', 'English'), ('hindi', 'Hindi'), ('marathi', 'Marathi'), ('gujarati', 'Gujarati'), ('telugu', 'Telugu'), ('other', 'Other')], max_length=50, null=True),
        ),
    ]
