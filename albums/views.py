from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Album
from django.db import models
from .serializers import AlbumListSerializer, AlbumDetailSerializer, ReviewsCreateSerializer, CreateRatingSerializer
from .service import get_client_ip


class AlbumListView(APIView):

    def get(self, request):
        albums = Album.objects.filter(draft=False).annotate(
            rating_user=models.Count('rating', filter=models.Q(rating__ip=get_client_ip(request)))
        ).annotate(
            middle_star=models.Sum(models.F('rating__star')) / models.Count(models.F('rating'))
        )
        serializer = AlbumListSerializer(albums, many=True)
        return Response(serializer.data)


class AlbumDetailView(APIView):

    def get(self, request, pk):
        album = Album.objects.get(draft=False, id=pk)
        serializer = AlbumDetailSerializer(album)
        return Response(serializer.data)


class ReviewsCreateView(APIView):
    def post(self, request):
        review = ReviewsCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
