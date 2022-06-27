import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist

from .models import Pokemon, PokemonEntity


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
    pokemons = Pokemon.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        local_time = localtime()
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lt=local_time,
                                                        disappeared_at__gt=local_time)

        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.image}')
            )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_image = None
        if pokemon.image:
            pokemon_image = request.build_absolute_uri(f'/media/{pokemon.image}')

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

    pokemon_info = {
        "pokemon_id": pokemon_id,
        "title_ru": pokemon.title_ru,
        'title_en': pokemon.title_en,
        "title_jp": pokemon.title_jp,
        'description': pokemon.description,
        "img_url": request.build_absolute_uri(f'/media/{pokemon.image}'),
        "entities": [],
    }

    pokemon_next_evolution = pokemon.next_evolution.first()
    if pokemon_next_evolution:
        pokemon_info["next_evolution"] = {
            "title_ru": pokemon_next_evolution,
            "pokemon_id": pokemon_next_evolution.id,
            "img_url": request.build_absolute_uri(f'/media/{pokemon_next_evolution.image}')
        }

    if pokemon.previous_evolution:
        pokemon_info["previous_evolution"] = {
            "title_ru": pokemon.previous_evolution.title_ru,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(f'/media/{pokemon.previous_evolution.image}')
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
