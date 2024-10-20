# Generated by Django 4.2.9 on 2024-10-19 13:59

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_user_date_deleted_user_first_name_user_last_name_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Client",
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
                ("name", models.CharField(max_length=256, verbose_name="Client name")),
                (
                    "national_id",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="Client ID"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Enter a valid email address.",
                                regex="^(?![.-])[a-zA-Z0-9._%+-]+(?<![.-])@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                            )
                        ],
                        verbose_name="email address",
                    ),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True,
                        max_length=128,
                        null=True,
                        region=None,
                        unique=True,
                        verbose_name="Phone Number of user",
                    ),
                ),
                (
                    "paid_money",
                    models.FloatField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Money which user already paid ",
                    ),
                ),
                (
                    "money_left",
                    models.FloatField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="left Money which user must  pay ",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="craeted at"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Compnay",
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
                    "name",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="company name"
                    ),
                ),
                (
                    "subdomain",
                    models.CharField(
                        max_length=256, unique=True, verbose_name="Company Subdomain"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="craeted at"
                    ),
                ),
            ],
        ),
    ]
