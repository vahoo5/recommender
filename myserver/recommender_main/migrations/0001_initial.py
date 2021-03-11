# Generated by Django 3.1.7 on 2021-03-05 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english', models.CharField(max_length=150)),
                ('synonyms', models.CharField(max_length=300)),
                ('japanese', models.CharField(max_length=150)),
                ('kind', models.CharField(max_length=20)),
                ('episodes', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('aired', models.CharField(max_length=50)),
                ('premiered', models.CharField(max_length=50)),
                ('broadcast', models.CharField(max_length=100)),
                ('producers', models.CharField(max_length=500)),
                ('licensors', models.CharField(max_length=100)),
                ('studios', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=50)),
                ('genres', models.CharField(max_length=150)),
                ('duration', models.CharField(max_length=50)),
                ('rating', models.CharField(max_length=50)),
                ('score', models.CharField(max_length=50)),
                ('ranked', models.CharField(max_length=20)),
                ('popularity', models.CharField(max_length=20)),
                ('members', models.IntegerField()),
                ('favorites', models.IntegerField()),
                ('name', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('url', models.CharField(max_length=200)),
            ],
        ),
    ]
