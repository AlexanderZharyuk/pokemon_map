# Generated by Django 3.1.14 on 2022-06-24 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='next_evolution',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
        ),
    ]
