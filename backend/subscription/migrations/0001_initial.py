# Generated by Django 5.0.4 on 2024-04-18 16:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('prev_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stripe_id', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('youtube', models.BooleanField(default=True)),
                ('spotify', models.BooleanField(default=False)),
                ('ai_transcription', models.BooleanField(default=False)),
                ('max_length', models.IntegerField(default=15)),
                ('max_result', models.IntegerField(default=2)),
                ('duration', models.IntegerField()),
                ('price', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.price')),
            ],
        ),
    ]
