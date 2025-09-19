import datetime

from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from yaml import serialize

from library.models import Book, Borrowing
from library.serializers import (
    BookSerializer,
    BorrowingListSerializer,
    BorrowingSerializerPost,
    BorrowingSerializerUpdate
)
from user.models import User

BOOK_URL=reverse("library:book-list")
BORROWING_URL=reverse("library:borrowing-list")


class UnauthenticatedUserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list(self):
        response = self.client.post(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_borrowing_list(self):
        response = self.client.get(BORROWING_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AuthenticatedUserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user_admin = User.objects.create_user(
            password="testpass", email="admin@admin.com", is_staff=True
        )
        self.user_nonadmin = User.objects.create_user(
            password="testpass", email="nonadmin@nonadmin.com"
        )

    def authenticate_as_admin(self):
        self.client.force_authenticate(user=self.user_admin)

    def authenticate_as_nonadmin(self):
        self.client.force_authenticate(user=self.user_nonadmin)

    def test_book_list_as_admin(self):
        self.authenticate_as_admin()
        response = self.client.get(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_as_admin(self):
        payload = {
            "title": "book1",
            "author": "me",
            "cover": "HARD",
            "inventory": 10,
        }
        self.authenticate_as_admin()
        response = self.client.post(BOOK_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_book_as_nonadmin(self):
        self.authenticate_as_nonadmin()
        response = self.client.post(BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_borrowing_by_user_id(self):
        self.client.force_authenticate(user=self.user_admin)
        book = Book.objects.create(
            title="book1",
            author="me",
            cover="HARD",
            inventory=10,
        )
        borrowing = Borrowing.objects.create(
            book_id=book.id,
            borrow_date=datetime.date.today(),
            expected_return_date=datetime.date.today(),
            is_active=True,
            user_id=self.user_admin.id,
        )
        res = self.client.get(BORROWING_URL, {"user_id": self.user_admin.id})

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer = BorrowingListSerializer([borrowing], many=True)
        self.assertEqual(res.data, serializer.data)

    def test_filter_borrowing_by_is_active_status(self):
        self.client.force_authenticate(user=self.user_admin)

        book = Book.objects.create(
            title="book1",
            author="me",
            cover="HARD",
            inventory=10,
        )
        borrowing = Borrowing.objects.create(
            book_id=book.id,
            borrow_date=datetime.date.today(),
            expected_return_date=datetime.date.today(),
            is_active=True,
            user_id=self.user_admin.id,
        )

        res = self.client.get(BORROWING_URL, {"is_active": "true"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = BorrowingListSerializer([borrowing], many=True)
        self.assertEqual(res.data, serializer.data)


