from django.urls import path, include
from rest_framework import routers

from .views import (
    BookListView,
    BorrowingListView,
)

app_name = "library"
router = routers.DefaultRouter()

router.register("books", BookListView)
router.register("borrowings", BorrowingListView)

urlpatterns = [
    path("", include(router.urls)),
]
