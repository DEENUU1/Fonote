# Generated by Django 5.0.4 on 2024-04-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0012_alter_usersubscription_status_order_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='invoice_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='invoice_url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]