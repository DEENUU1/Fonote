# Generated by Django 5.0.4 on 2024-04-25 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0017_order_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='change_lang',
            field=models.BooleanField(default=False),
        ),
    ]
