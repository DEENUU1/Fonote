# Generated by Django 5.0.4 on 2024-04-18 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_alter_order_id_alter_usersubscription_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='prev_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]
