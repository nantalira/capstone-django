from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer


# Create your views here.
def index(request):
    return render(request, 'index.html', {})


# Menu API Views using DRF Generic Views
class MenuItemsView(generics.ListCreateAPIView):
    """
    GET: List all menu items (public access)
    POST: Create a new menu item (authenticated users only)
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions for this view.
        GET requests are public, POST requires authentication.
        """
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single menu item (public access)
    PUT/PATCH: Update a menu item (authenticated users only)
    DELETE: Delete a menu item (authenticated users only)
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions for this view.
        GET requests are public, PUT/PATCH/DELETE require authentication.
        """
        if self.request.method == 'GET':
            permission_classes = []
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


# Booking API Views (Authentication Required)
class BookingView(generics.ListCreateAPIView):
    """
    GET: List all bookings (authenticated users only)
    POST: Create a new booking (authenticated users only)
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all the bookings
        for the currently authenticated user.
        """
        user = self.request.user
        return Booking.objects.filter(user=user)


class SingleBookingView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single booking (authenticated users only)
    PUT/PATCH: Update a booking (authenticated users only)  
    DELETE: Delete a booking (authenticated users only)
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all the bookings
        for the currently authenticated user.
        """
        user = self.request.user
        return Booking.objects.filter(user=user)