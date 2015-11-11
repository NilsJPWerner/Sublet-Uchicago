from django.contrib import admin

from .models import listing

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
	model = listing
	readonly_fields=('id',)

admin.site.register(listing, ListingAdmin)