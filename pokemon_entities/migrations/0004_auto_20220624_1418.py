# Generated by Django 3.1.14 on 2022-06-24 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0003_auto_20220624_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemonelementtype',
            name='pokemon_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pokemon_entities.pokemon'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='element_type',
            field=models.ManyToManyField(to='pokemon_entities.PokemonElementType', verbose_name='Стихии покемона'),
        ),
    ]
