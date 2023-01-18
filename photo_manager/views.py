import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Photo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status, generics
from .serializers import PhotoSerializer, PhotosListSerializer
from .parsers import ImageUploadParser
from .filters import PhotoFilter, IsOwnerFilterBackend
from django_filters.rest_framework import DjangoFilterBackend
from itertools import chain


class PhotosListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotosListSerializer
    filter_backends = [IsOwnerFilterBackend]
    filterset_class = PhotoFilter


class PhotoViev(APIView):
    parser_class = (ImageUploadParser,)

    def post(self, request, format=None):
        if 'photo' not in request.data:
            raise ParseError("Empty content")
        s = PhotoSerializer(data=request.data)
        if s.is_valid():
            s.validated_data['available'] = True
            s.save()
            return Response({'errors': None}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': s.errors}, status=status.HTTP_400_BAD_REQUEST)


def autocompliete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET['person']
        queryset = Photo.objects.all()
        queryset = queryset.filter(meta__marked_persons__icontains=query)
        result = [q.meta["marked_persons"] for q in queryset]
    return JsonResponse({'result': list(set(chain.from_iterable(result)))})
