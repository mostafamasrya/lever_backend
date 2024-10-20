# Generated by Django 4.2.9 on 2024-10-20 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0006_rename_compnay_client_company"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="client",
            name="company",
        ),
        migrations.CreateModel(
            name="ClientCompany",
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
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="client_companies",
                        to="users.client",
                    ),
                ),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="company_clients",
                        to="users.company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Client-Company Relationship",
                "verbose_name_plural": "Client-Company Relationships",
                "unique_together": {("client", "company")},
            },
        ),
    ]
