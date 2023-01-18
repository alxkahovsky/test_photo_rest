from django_filters import rest_framework as filters
from .models import Photo
from django.shortcuts import render
from django.template import loader


class IsOwnerFilterBackend(filters.DjangoFilterBackend):
    pass


class PhotoFilter(filters.FilterSet):
    available = filters.BooleanFilter(field_name='available', method='check_avilable', label='Активность')
    date = filters.DateFilter(field_name='created__date', method='filter_by_date', label='Дата')
    date_lte = filters.DateFilter(field_name='created__date', method='filter_date_lte', label='Дата до')
    date_gte = filters.DateFilter(field_name='created__date', method='filter_date_gte', label='Дата после')
    person = filters.CharFilter(field_name='meta', method='filter_person', label='По имени')

    def check_avilable(self, queryset, field_name, value):
        print(queryset)
        print(field_name)
        print(value)
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
        print(value)
        queryset = queryset.filter(meta__marked_persons__icontains=value)
        print(queryset)
        return queryset

    class Meta:
        model = Photo
        fields = ['available']


