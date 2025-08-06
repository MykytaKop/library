from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .permissions import IsAdminOrIfAuthenticatedReadOnly

from library.models import Book, Borrowing
from library.serializers import (
    BookSerializer,
    BorrowingListSerializer,
    BorrowingSerializerPost,
    BorrowingSerializerUpdate,
)


class BookListView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]


class BorrowingListView(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        borrowing = Borrowing.objects.all()
        is_active_filter = self.request.query_params.get("is_active")

        if is_active_filter and is_active_filter.lower() == "true":
            borrowing = borrowing.filter(is_active=True)
        elif is_active_filter and is_active_filter.lower() == "false":
            borrowing = borrowing.filter(is_active=False)

        if self.request.user.is_staff:
            user_id_filter = self.request.query_params.get("user_id")
            if user_id_filter:
                try:
                    borrowing = borrowing.filter(user=int(user_id_filter))
                except Exception as w:
                    raise ValidationError(w)
        return borrowing

    def get_serializer_class(self):
        if self.action == "return_book":
            return BorrowingSerializerUpdate
        elif self.request.method == "GET":
            return BorrowingListSerializer
        elif self.request.method == "POST":
            return BorrowingSerializerPost
        return BorrowingSerializerUpdate

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        if book.inventory <= 0:
            raise ValidationError("This book is not available right now.")

        serializer.save(user=self.request.user)

        book.inventory -= 1
        book.save()

    @action(
        detail=True,
        methods=["post"],
        url_path="return",
        serializer_class=BorrowingSerializerUpdate,
    )
    def return_book(self, request, pk=None):
        borrowing = self.get_object()

        serializer = self.get_serializer(borrowing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if borrowing.actual_return_date:
            return Response(
                {"detail": "Book already returned."}, status=status.HTTP_400_BAD_REQUEST
            )

        borrowing.actual_return_date = serializer.validated_data["actual_return_date"]
        borrowing.is_active = False

        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()

        return Response(
            {"detail": "Book returned successfully."}, status=status.HTTP_200_OK
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="The ID of the user to borrow",
            ),
            OpenApiParameter(
                name="is_active",
                description="Whether the user is active or not",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response
