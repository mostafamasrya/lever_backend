# Generated by Django 4.2.9 on 2024-10-20 18:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_client_compnay"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="compnay",
            new_name="company",
        ),
    ]
