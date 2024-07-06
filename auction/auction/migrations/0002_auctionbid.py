# Generated by Django 5.0.6 on 2024-07-06 07:29

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auction", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AuctionBid",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "auction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auction.auction",
                    ),
                ),
            ],
        ),
    ]
