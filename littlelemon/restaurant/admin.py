from django.contrib import admin
from .models import Menu, Booking


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'inventory']
    list_filter = ['price']
    search_fields = ['title']
    ordering = ['title']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'no_of_guest', 'bookingdate']
    list_filter = ['bookingdate', 'no_of_guest']
    search_fields = ['name', 'user__username']
    ordering = ['-bookingdate']
