# Generated by Django 3.1.5 on 2021-02-04 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210204_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='bid_listing',
        ),
        migrations.AddField(
            model_name='bid',
            name='bid_listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bid', to='auctions.auctionlisting'),
            preserve_default=False,
        ),
    ]
