from django.db import models  # noqa F401


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='[RU] Имя покемона')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='[EN] Имя покемона')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='[JP] Имя покемона')
    image = models.ImageField(upload_to='pokemon_images', null=True, verbose_name='Фото покемона')
    description = models.TextField(blank=True, verbose_name='Описание покемона')
    previous_evolution = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                           related_name='evolution', verbose_name='Из кого покемон эволюционирует')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Имя покемона')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(verbose_name='Время появления покемона')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения покемона')
    level = models.IntegerField(default=0, verbose_name='Уровень')
    health = models.IntegerField(default=0, verbose_name='Здоровье')
    strength = models.IntegerField(default=0, verbose_name='Сила')
    defence = models.IntegerField(default=0, verbose_name='Защита')
    stamina = models.IntegerField(default=0, verbose_name='Выносливость')

    def __str__(self):
        return f'{self.appeared_at}. {self.pokemon}'
