from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Album
from .serializers import AlbumListSerializer, AlbumDetailSerializer, ReviewsCreateSerializer


class AlbumListView(APIView):

    def get(self, request):
        albums = Album.objects.filter(draft=False)
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
