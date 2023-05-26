# Generated by Django 4.0.4 on 2023-05-24 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("dinosaurs", "0003_remove_dinosaur_favourites_dinosaur_favourite"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dinosaur",
            name="favourite",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="dinosaurs.favourite",
            ),
        ),
    ]