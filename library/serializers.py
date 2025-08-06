from rest_framework import serializers

from user.serializers import UserSerializer
from .models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "cover", "inventory"]


class BorrowingListSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = Borrowing
        fields = [
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        ]


class BorrowingSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "expected_return_date",
            "book",
        ]


class BorrowingSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = [
            "id",
            "actual_return_date",
        ]
