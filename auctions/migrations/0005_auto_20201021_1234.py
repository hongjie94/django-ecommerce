# Generated by Django 3.1.2 on 2020-10-21 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201021_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='bid_amount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
