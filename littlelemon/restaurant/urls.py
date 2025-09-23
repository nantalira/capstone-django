from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    
    # API endpoints
    path('api/menu-items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('api/menu-items/<int:pk>/', views.SingleMenuItemView.as_view(), name='menu-item-detail'),
    
    # Booking API endpoints (require authentication)
    path('api/bookings/', views.BookingView.as_view(), name='bookings'),
    path('api/bookings/<int:pk>/', views.SingleBookingView.as_view(), name='booking-detail'),
]
