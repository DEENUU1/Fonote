# Generated by Django 5.0.4 on 2024-04-20 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ai', '0004_inputdata_language_alter_inputdata_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fragment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.FloatField()),
                ('end_time', models.FloatField()),
                ('order', models.IntegerField()),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'Fragment',
                'verbose_name_plural': 'Fragments',
            },
        ),
        migrations.AlterField(
            model_name='inputdata',
            name='language',
            field=models.CharField(choices=[('Danish', 'Danish'), ('Czech', 'Czech'), ('Dutch', 'Dutch'), ('English', 'English'), ('German', 'German'), ('Italian', 'Italian'), ('Japanese', 'Japanese'), ('Korean', 'Korean'), ('Polish', 'Polish'), ('Spanish', 'Spanish'), ('French', 'French')], max_length=25),
        ),
        migrations.AddField(
            model_name='inputdata',
            name='youtube_fragments',
            field=models.ManyToManyField(blank=True, null=True, to='ai.fragment'),
        ),
    ]
