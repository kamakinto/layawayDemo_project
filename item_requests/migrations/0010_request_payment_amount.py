# Generated by Django 2.0.2 on 2018-06-24 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item_requests', '0009_auto_20180622_0524'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]
