# Generated by Django 5.0.6 on 2024-07-06 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auction", "0002_auctionbid"),
    ]

    operations = [
        migrations.AddField(
            model_name="lot",
            name="image",
            field=models.ImageField(default=None, null=True, upload_to="lots/"),
        ),
    ]
