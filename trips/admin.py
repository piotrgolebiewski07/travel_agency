from django.contrib import admin
from .models import Trip, TripImage


class TripImageInline(admin.TabularInline):
    model = TripImage
    extra = 1


class TripAdmin(admin.ModelAdmin):
    inlines = [TripImageInline]


admin.site.register(Trip, TripAdmin)

