from django.contrib import admin
from .models import Trip, TripImage, Review, ContactMessage


class TripImageInline(admin.TabularInline):
    model = TripImage
    extra = 1


class TripAdmin(admin.ModelAdmin):
    inlines = [TripImageInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "trip", "rating", "created_at")


admin.site.register(Trip, TripAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(ContactMessage)

