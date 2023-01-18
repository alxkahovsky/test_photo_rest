from django.db import models
from django.utils import timezone
from geopy.geocoders import Nominatim


def defult_meta() -> dict:
    """
    Возвращает defaul-ное значение meta-данных, если они не указаны при создании записи.
    :return: dict
    """
    return {"location": None,
            "description": None,
            "marked_persons": []}


class Photo(models.Model):
    photo = models.ImageField(upload_to='photos', blank=True,
                              verbose_name='Фотография')
    meta = models.JSONField(verbose_name='Метаданные', default=defult_meta, blank=True, null=True)
    available = models.BooleanField(default=True, verbose_name='Доступно?')
    created = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')
    updated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='Дата ред-ия записи')

    def location_city(self) -> str:
        """
        метод возвращает текстовое представление города по координатам
        :return: str
        """
        if self.meta['location']:
            geolocator = Nominatim(user_agent="Test_photo_rest")
            location = geolocator.reverse(self.meta['location'], language='en')
            # location.raw возвращает архив, но ключ city может отсутствовать, поэтому используем .get()
            return location.raw['address'].get('city')

    def marked_persons(self) -> list:
        if self.meta['marked_persons']:
            return self.meta['marked_persons']

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'Фото №{self.id}'

