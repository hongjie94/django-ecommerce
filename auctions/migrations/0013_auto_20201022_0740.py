# Generated by Django 3.1.2 on 2020-10-21 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(default='NONE', max_length=65),
        ),
    ]