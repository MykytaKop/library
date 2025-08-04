from django.urls import path, include
from rest_framework import routers

from library.views import BookListView

app_name = "library"
router = routers.DefaultRouter()

router.register("books", BookListView)

urlpatterns = [
    path("", include(router.urls)),
]