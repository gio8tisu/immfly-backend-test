# Generated by Django 4.0.4 on 2022-05-31 11:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('language', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rating', models.IntegerField()),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contents.channel')),
            ],
        ),
    ]
