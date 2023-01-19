from django_filters import rest_framework as filters
from .models import Photo
from django.shortcuts import render
from django.template import loader
from django.db.models import Q
from geopy.distance import geodesic
from decimal import Decimal
from django.http import Http404


class IsOwnerFilterBackend(filters.DjangoFilterBackend):
    """
    Переопределяем DjangoFilterBackends, таким образом этот класс будет подтягивать кастомные шаблоны
    из папки 'templates/django_filters/rest_framework' в котором добавлена форма поиска с автозаполнением.
    """
    pass


class PhotoFilter(filters.FilterSet):
    available = filters.BooleanFilter(field_name='available', method='check_avilable', label='Активность')
    date = filters.DateFilter(field_name='created__date', method='filter_by_date', label='Дата')
    date_lte = filters.DateFilter(field_name='created__date', method='filter_date_lte', label='Дата до')
    date_gte = filters.DateFilter(field_name='created__date', method='filter_date_gte', label='Дата после')
    person = filters.CharFilter(field_name='meta', method='filter_person', label='По имени')
    radius = filters.BaseCSVFilter(field_name='meta', method='filter_location', label='По точке и радиус')

    def check_avilable(self, queryset, field_name, value):
        queryset = queryset.filter(available=value)
        return queryset

    def filter_by_date(self, queryset, field_name, value):
        queryset = queryset.filter(created__date=value)
        return queryset

    def filter_date_lte(self, queryset, field_name, value):
        queryset = queryset.filter(created__date__lte=value)
        return queryset

    def filter_date_gte(self, queryset, field_name, value):
        queryset = queryset.filter(created__date__gte=value)
        return queryset

    def filter_person(self, queryset, field_name, value):
        queryset = queryset.filter(meta__marked_persons__icontains=value)
        return queryset

    def filter_location(self, queryset, field_name, value):
        """
        Поскольку мы используем BaseCSVFilter то параметр value будет поступать на вход в виде списка (list).
        """
        if len(value) < 2:
            raise Http404
        position = tuple(value[:2])
        radius = 0 if len(value) < 3 else float(value[2])
        # отфильтровываем объекты без мета данных
        queryset = queryset.filter(meta__isnull=False)
        # создаем список объектов с геолокацией
        photos_with_loc = [q for q in queryset if q.meta.get('location')]
        photos_ids_result = []
        for photo in photos_with_loc:
            photo_location = tuple(float(i) for i in photo.meta['location'].split(','))
            # получаем геодезическое рассояние между точками "геометка_на_фото" и "геометка_запроса"
            distance = geodesic(photo_location, position).kilometers
            if distance <= radius:
                photos_ids_result.append(photo.id)
        queryset = queryset.filter(id__in=photos_ids_result)
        return queryset

    class Meta:
        model = Photo
        fields = ['available']


