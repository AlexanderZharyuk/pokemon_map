from django.db import models


class Pokemon(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name='[RU] Имя покемона')
    title_en = models.CharField(max_length=200, verbose_name='[EN] Имя покемона', blank=True)
    title_jp = models.CharField(max_length=200, verbose_name='[JP] Имя покемона', blank=True)
    image = models.ImageField(upload_to='pokemon_images', null=True, verbose_name='Фото покемона')
    description = models.TextField(verbose_name='Описание покемона')
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
    level = models.IntegerField(verbose_name='Уровень', null=True, blank=True)
    health = models.IntegerField(verbose_name='Здоровье', null=True, blank=True)
    strength = models.IntegerField(verbose_name='Сила', null=True, blank=True)
    defence = models.IntegerField(verbose_name='Защита', null=True, blank=True)
    stamina = models.IntegerField(verbose_name='Выносливость', null=True, blank=True)

    def __str__(self):
        return f'{self.appeared_at}. {self.pokemon}'
