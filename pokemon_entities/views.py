import os

import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity
from pogomap.settings import MEDIA_URL


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    local_time = localtime()
    pokemons = list(Pokemon.objects.all())
    pokemons_entities = list(PokemonEntity.objects.filter(appeared_at__lt=local_time, disappeared_at__gt=local_time))

    for pokemon_entity in pokemons_entities:
        image_path = os.path.join(MEDIA_URL, str(pokemon_entity.pokemon.image))
        add_pokemon(folium_map, pokemon_entity.lat, pokemon_entity.lon,
                    request.build_absolute_uri(image_path))

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image = None
        if pokemon.image:
            image_path = os.path.join(MEDIA_URL, str(pokemon.image))
            pokemon_image = request.build_absolute_uri(image_path)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    local_time = localtime()
    pokemon_entities = pokemon.pokemon_entities.filter(appeared_at__lt=local_time, disappeared_at__gt=local_time)
    image_path = os.path.join(MEDIA_URL, str(pokemon.image))

    pokemon_info = {
        "pokemon_id": pokemon_id,
        "title_ru": pokemon.title_ru,
        'title_en': pokemon.title_en,
        "title_jp": pokemon.title_jp,
        'description': pokemon.description,
        "img_url": request.build_absolute_uri(image_path),
        "entities": [],
    }

    pokemon_next_evolution = pokemon.next_evolution.first()
    if pokemon_next_evolution:
        image_path = os.path.join(MEDIA_URL, str(pokemon_next_evolution.image))
        pokemon_info["next_evolution"] = {
            "title_ru": pokemon_next_evolution,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": request.build_absolute_uri(image_path)
        }

    if pokemon.previous_evolution:
        image_path = os.path.join(MEDIA_URL, str(pokemon.previous_evolution.image))
        pokemon_info["previous_evolution"] = {
            "title_ru": pokemon.previous_evolution.title_ru,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(image_path)
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        pokemon_info["entities"] = {
            "level": pokemon_entity.level,
            "lat": pokemon_entity.lat,
            "lon": pokemon_entity.lon
        }

        add_pokemon(
            folium_map, pokemon_info["entities"]['lat'],
            pokemon_info["entities"]['lon'],
            pokemon_info['img_url']
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
