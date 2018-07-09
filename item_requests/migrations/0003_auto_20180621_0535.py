# Generated by Django 2.0.2 on 2018-06-21 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_requests', '0002_auto_20180621_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='request',
            name='title',
            field=models.CharField(default='layaway request', max_length=120),
        ),
    ]