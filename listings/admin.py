from django.contrib import admin
from .models import *


class ListingAdmin(admin.ModelAdmin):
    model = Listing


class PhotoAdmin(admin.ModelAdmin):
    model = Photo

admin.site.register(Listing, ListingAdmin)
admin.site.register(Photo, PhotoAdmin)