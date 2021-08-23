from django.db import models
from datetime import date

from django.db.models import Avg
from django.urls import reverse


class Band(models.Model):
    name = models.CharField('Группа', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def get_albums(self):
        albums = Album.objects.filter(category=self)
        return albums


class ArtistLabel(models.Model):
    name = models.CharField('Имя', max_length=256)
    description = models.TextField('Описание')
    age = models.PositiveSmallIntegerField('Возраст', default=0)
    image = models.ImageField('Изображение', upload_to='artists_labels/')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Музыкант - лейбл'
        verbose_name_plural = 'Музыканты и лейблы'


class Genre(models.Model):
    name = models.CharField('Название', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Album(models.Model):
    title = models.CharField('Название', max_length=256)
    description = models.TextField('Описание')
    cover = models.ImageField('Обложка', upload_to='albums/')
    year = models.PositiveSmallIntegerField('Год выхода')
    country = models.CharField('Страна', max_length=50)
    label = models.ManyToManyField(ArtistLabel, verbose_name='Лейбл', related_name='album_label')
    artist = models.ManyToManyField(ArtistLabel, verbose_name='Музыкант', related_name='album_artist')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    premiere = models.DateField('Дата выхода', default=date.today)
    streams = models.PositiveIntegerField('Прослушиваний', default=0)
    category = models.ForeignKey(Band, verbose_name='Группа', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=256, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def get_absolute_url(self):
        return reverse('album_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    def average_rating(self):
        reviews = Rating.objects.filter(album=self).aggregate(average=Avg('star'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg


class Images(models.Model):
    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField('Изображение', upload_to='covers/')
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-value']


class Rating(models.Model):
    ip = models.CharField('IP адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, verbose_name='Альбом')

    def __str__(self):
        return f'{self.star} - {self.album}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.album}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

