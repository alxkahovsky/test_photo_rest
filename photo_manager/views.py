import json
from itertools import chain
from django.http import HttpResponse, JsonResponse, Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import PhotoSerializer, PhotosListSerializer
from .models import Photo
from .parsers import ImageUploadParser
from .filters import PhotoFilter, IsOwnerFilterBackend
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin


class PhotosListView(ListModelMixin, CreateModelMixin, RetrieveModelMixin,  viewsets.GenericViewSet):
    queryset = Photo.objects.all()
    action_serializers = {'list': PhotosListSerializer, 'retrieve': PhotoSerializer, "create": PhotoSerializer}
    filter_backends = [IsOwnerFilterBackend]
    filterset_class = PhotoFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super(PhotosListView, self).get_serializer_class()

    def create(self, request, *args, **kwargs):
        if 'photo' not in request.data:
            raise ParseError("Empty content")
        s = self.get_serializer_class()(data=request.data)
        if s.is_valid():
            s.validated_data['available'] = True
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': s.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.get(id=kwargs['pk'])
        except Photo.DoesNotExist:
            raise Http404
        s = self.get_serializer_class()(queryset)
        return Response(s.data)


def autocompliete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET['person']
        queryset = Photo.objects.filter(meta__isnull=False).filter(meta__marked_persons__icontains=query)
        result = [q.meta["marked_persons"] for q in queryset]
        result = list(set(chain.from_iterable(result)))
        result = [r for r in result if r.startswith(query)]
    return JsonResponse({'result': result})
