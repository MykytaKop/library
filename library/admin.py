from django.contrib import admin

from library.models import Borrowing, Book, User

admin.site.register(Borrowing)
admin.site.register(Book)
admin.site.register(User)
