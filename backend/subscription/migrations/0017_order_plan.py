# Generated by Django 5.0.4 on 2024-04-24 13:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0016_plan_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subscription.plan'),
        ),
    ]