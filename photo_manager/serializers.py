from rest_framework import serializers
from .models import Photo


class PhotosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ['meta']


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

    def validate(self, data):
        """
        Валидация json meta данных по полям
        """
        raw_meta = data.get('meta')
        if raw_meta:
            if sorted(raw_meta.keys()) == sorted(['location', 'description', 'marked_persons']):
                if not isinstance(raw_meta['marked_persons'], list or tuple):
                    raise serializers.ValidationError('"marked_persons" must be list or tuple')
                return data
            else:
                raise serializers.ValidationError('Keys must be: "location, description, marked_persons"')
        else:
            data['meta'] = {"location": None, "description": None, "marked_persons": []}
            return data
