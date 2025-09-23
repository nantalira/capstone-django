from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from decimal import Decimal
from .models import Menu, Booking
from .serializers import MenuSerializer


class MenuModelTest(TestCase):
    """Test cases for Menu model"""
    
    def test_get_item(self):
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        self.assertEqual(str(item), "IceCream : 80")


class MenuAPITest(APITestCase):
    """Test cases for Menu API endpoints"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
        
        # Create test menu items
        self.menu_item1 = Menu.objects.create(
            title="Test Item 1",
            price=Decimal('15.99'),
            inventory=10
        )
        self.menu_item2 = Menu.objects.create(
            title="Test Item 2", 
            price=Decimal('12.50'),
            inventory=5
        )
        
    def test_get_menu_items(self):
        """Test retrieving menu items (public access)"""
        url = reverse('menu-items')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_create_menu_item_authenticated(self):
        """Test creating menu item with authentication"""
        url = reverse('menu-items')
        data = {
            'title': 'New Test Item',
            'price': '18.99',
            'inventory': 15
        }
        
        # Include authentication token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)
        
    def test_create_menu_item_unauthenticated(self):
        """Test creating menu item without authentication should fail"""
        url = reverse('menu-items')
        data = {
            'title': 'New Test Item',
            'price': '18.99',
            'inventory': 15
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BookingAPITest(APITestCase):
    """Test cases for Booking API endpoints"""
    
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            password='testpass123'
        )
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        
        # Create test booking for user1
        self.booking1 = Booking.objects.create(
            user=self.user1,
            name="Test Booking 1",
            no_of_guest=4,
            bookingdate="2024-12-25 19:00:00"
        )
        
    def test_get_bookings_authenticated(self):
        """Test retrieving bookings for authenticated user"""
        url = reverse('bookings')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_get_bookings_unauthenticated(self):
        """Test retrieving bookings without authentication should fail"""
        url = reverse('bookings')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_booking_authenticated(self):
        """Test creating booking with authentication"""
        url = reverse('bookings')
        data = {
            'name': 'New Test Booking',
            'no_of_guest': 2,
            'bookingdate': '2024-12-31 20:00:00'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.filter(user=self.user1).count(), 2)
        
    def test_user_can_only_see_own_bookings(self):
        """Test that users can only see their own bookings"""
        # Create booking for user2
        Booking.objects.create(
            user=self.user2,
            name="User2 Booking",
            no_of_guest=3,
            bookingdate="2024-12-26 18:00:00"
        )
        
        # User1 should only see their own booking
        url = reverse('bookings')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Test Booking 1")


class MenuSerializerTest(TestCase):
    """Test cases for Menu serializer"""
    
    def test_menu_serializer(self):
        """Test Menu serializer with valid data"""
        data = {
            'title': 'Test Menu Item',
            'price': '19.99',
            'inventory': 20
        }
        
        serializer = MenuSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        menu_item = serializer.save()
        self.assertEqual(menu_item.title, 'Test Menu Item')
        self.assertEqual(menu_item.price, Decimal('19.99'))
        self.assertEqual(menu_item.inventory, 20)
