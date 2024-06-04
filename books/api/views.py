from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from books.api.permissions import IsAdminOrOperator
from books.api.serializers import BookSerializer, RateBookSerializer
from books.models import Book, StarsBook


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


class RateBookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = RateBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # example:
    # {
    #     "book": 1,
    #     "user": 1,
    #     "star": 5,
    #     "description": "Yaxshi kitob ekan"
    # }
