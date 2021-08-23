from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.utils.safestring import mark_safe

from django import forms

from .models import *


class AlbumAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Album
        fields = '__all__'


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name',)


class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('name', 'email',)


class AlbumImagesInLine(admin.TabularInline):
    model = Images
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="auto" height="60"')

    get_image.short_description = 'Фото'


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year',)
    search_fields = ('title', 'category__name')
    inlines = [AlbumImagesInLine, ReviewInLine]
    form = AlbumAdminForm
    save_on_top = True
    save_as = True
    list_editable = ('draft',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'album', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')


@admin.register(ArtistLabel)
class ArtistLabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="auto" height="60"')

    get_image.short_description = 'Фото'


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="auto" height="60"')

    get_image.short_description = 'Фото'


admin.site.register(RatingStar)


@admin.register(Rating)
class AlbumRating(admin.ModelAdmin):
    list_display = ('ip', 'star', 'album')


admin.site.site_title = 'Панель администрирования'
admin.site.site_header = 'Панель администрирования'
