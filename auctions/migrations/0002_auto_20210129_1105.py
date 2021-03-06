# Generated by Django 3.1.5 on 2021-01-29 19:05

import auctions.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionListing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=60)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('description', models.CharField(max_length=500)),
                ('active', models.BooleanField(default=True)),
                ('date_listed', models.DateTimeField(auto_now_add=True)),
                ('image', models.URLField(default=auctions.models.default_img, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=250)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_bid', models.DateTimeField(auto_now_add=True)),
                ('bid_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rn_category', to='auctions.category'),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='lister_user',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='rn_lister', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='rn_watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='winner_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rn_winner', to=settings.AUTH_USER_MODEL),
        ),
    ]
