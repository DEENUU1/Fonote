# Generated by Django 5.0.4 on 2024-05-05 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0022_plan_web'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='web',
        ),
    ]