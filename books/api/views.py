from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

from books.api.permissions import IsAdminOrOperator
from books.api.serializers import BookSerializer
from books.models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get', 'post', 'put', 'delete']
    authentication_classes = (JWTAuthentication, SessionAuthentication)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return [IsAuthenticated(), ]
        else:
            return [IsAdminOrOperator(), ]

# class RateBookViewSet(viewsets.ModelViewSet):

