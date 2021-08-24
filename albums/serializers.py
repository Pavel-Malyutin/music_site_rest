from rest_framework import serializers

from .models import Album, Reviews


class AlbumListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('title', 'year', 'category')


class ReviewsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = ('name', 'text', 'parent')


class AlbumDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    label = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    artist = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewsSerializer(many=True)

    class Meta:
        model = Album
        exclude = ('draft', )
