# Generated by Django 5.0.4 on 2024-04-22 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0015_remove_plan_ai_transcription'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
