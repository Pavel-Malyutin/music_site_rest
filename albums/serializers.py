from rest_framework import serializers

from .models import Album, Reviews, Rating


class AlbumListSerializer(serializers.ModelSerializer):

    middle_star = serializers.IntegerField()
    rating_user = serializers.BooleanField()

    class Meta:
        model = Album
        fields = ('id', 'title', 'year', 'category', 'rating_user', 'middle_star')


class ReviewsCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reviews
        fields = '__all__'


class CreateRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating

class FilterReviewListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewsSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Reviews
        fields = ('name', 'text', 'children')


class AlbumDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    label = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    artist = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewsSerializer(many=True)

    class Meta:
        model = Album
        exclude = ('draft', )
