# Generated by Django 3.2.15 on 2022-10-05 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_youtubetest_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('sub_text', models.TextField(blank=True, null=True)),
                ('channel', models.TextField(blank=True, null=True)),
                ('img', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('start', models.TextField(blank=True, null=True)),
                ('duration', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'youtube',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='YoutubeReal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('sub_text', models.TextField(blank=True, null=True)),
                ('channel', models.TextField(blank=True, null=True)),
                ('img', models.TextField(blank=True, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('start', models.TextField(blank=True, null=True)),
                ('duration', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'youtube_real',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='YoutubeTest',
        ),
    ]