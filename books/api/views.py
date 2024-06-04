from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from books.api.permissions import IsAdminOrOperator
from books.api.serializers import BookSerializer, RateBookSerializer
from books.models import Book, StarsBook, StarsOfUsers
from rent.models import BookRent


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
        book = Book.objects.filter(id=request.data['book']).first()
        if not book:
            return Response({"message": "Kiritilgan kitob topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        rate = StarsOfUsers.objects.filter(user=request.user, book=book).first()
        if rate:
            return Response({"message": "Siz oldin bu kitobga baho berib bo'lgansiz"},
                            status=status.HTTP_200_OK)
        serializer = RateBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # example:
    # {
    #     "book": 1,
    #     "star": 5,
    #     "description": "Yaxshi kitob ekan"
    # }
