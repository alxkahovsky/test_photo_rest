import json
from itertools import chain
from django.http import HttpResponse, JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PhotoSerializer, PhotosListSerializer
from .models import Photo
from .parsers import ImageUploadParser
from .filters import PhotoFilter, IsOwnerFilterBackend


class PhotosListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotosListSerializer
    filter_backends = [IsOwnerFilterBackend]
    filterset_class = PhotoFilter


class PhotoViev(APIView):
    queryset = Photo.objects.all()
    parser_class = (ImageUploadParser,)
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, format=None):
        if 'photo' not in request.data:
            raise ParseError("Empty content")
        s = self.serializer_class(data=request.data)
        if s.is_valid():
            s.validated_data['available'] = True
            s.save()
            return Response({'errors': None}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': s.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        try:
            queryset = self.queryset.get(id=id)
        except Photo.DoesNotExist:
            raise Http404
        s = self.serializer_class(queryset)
        return Response(s.data)


def autocompliete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET['person']
        queryset = Photo.objects.all()
        queryset = queryset.filter(meta__marked_persons__icontains=query)
        result = [q.meta["marked_persons"] for q in queryset]
    return JsonResponse({'result': list(set(chain.from_iterable(result)))})
