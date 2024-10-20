# Generated by Django 4.2.9 on 2024-10-20 20:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_client_companies"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="companies",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="clients",
                through="users.ClientCompany",
                to="users.company",
            ),
        ),
    ]
