from django.shortcuts import render
from rest_framework import viewsets

from library.models import Book
from library.serializers import BookSerializer


class BookListView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer