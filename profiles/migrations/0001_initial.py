# Generated by Django 2.0.2 on 2018-05-31 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=250)),
                ('first_name', models.CharField(blank=True, max_length=250)),
                ('last_name', models.CharField(blank=True, max_length=250)),
                ('role', models.CharField(choices=[('admin', 'Administrator'), ('contributor', 'Contributor'), ('default_user', 'Default User')], default='default_user', max_length=100)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]