from django.urls import path

from . import views


urlpatterns = [
    path('album/', views.AlbumListView.as_view()),
    path('album/<int:pk>/', views.AlbumDetailView.as_view()),
    path('review/', views.ReviewsCreateView.as_view()),
]

