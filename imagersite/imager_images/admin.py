from django.contrib import admin
from imager_images.models import Photo
from imager_images.models import Album


class AlbumAdmin(admin.ModelAdmin):

    list_display = ('user', 'title', 'published')
    list_filter = ('user', )


admin.site.register(Album, AlbumAdmin)


class PhotoAdmin(admin.ModelAdmin):

    list_display = ('title', 'user', 'published')
    list_filter = ('user', )


admin.site.register(Photo, PhotoAdmin)
