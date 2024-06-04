from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from user.api.validators import check_phone_number
from user.models import RentalUser
from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOrOwner, IsOperatorOrSuperAdmin
from ..models import BookReservation, BookRent
from .serializers import BookReservationSerializer, BookRentSerializer, RentSerializer
from django.utils import timezone

from books.models import Book


class BookReservationViewSet(viewsets.ModelViewSet):
    queryset = BookReservation.objects.all()
    serializer_class = BookReservationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        book = Book.objects.filter(id=request.data['book']).first()
        if not book:
            return Response({"message": "Bunday kitob topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        if book.quantity < 1:
            return Response({"message": "Ushbu kitob hozirda kutubxonada mavjud emas"},
                            status=status.HTTP_200_OK)
        serializer = BookReservationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user'] = request.user
            book.quantity -= 1
            book.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        if request.user.user_type == "Customer":
            reservations = BookReservation.objects.filter(user=request.user.id).all()
        elif request.user.user_type == "Operator" or request.user.is_superuser:
            reservations = BookReservation.objects.all()
        page = self.paginate_queryset(reservations)
        if page is not None:
            serializer = self.get_paginated_response(BookReservationSerializer(page, many=True).data)
        else:
            serializer = BookReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrOwner, ])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        reservation.book.quantity += 1
        reservation.is_active = False
        reservation.save()
        return Response({'status': 'Bron bekor qilindi'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOperatorOrSuperAdmin, ])
    def confirm(self, request, pk=None):
        reservation = self.get_object()
        if not reservation.is_active:
            return Response(
                {'message': "Bron foydalanuvchi tomonidan bekor qilingan yoki olib ketish vaqti o'tib ketgan"})
        if reservation.is_confirmed:
            return Response({"message": "Ushbu kitob allaqachon tasdiqlangan"},
                            status=status.HTTP_200_OK)
        reservation.is_confirmed = True
        BookRent.objects.create(
            user=reservation.user,
            book=reservation.book,
            return_date=reservation.expiration_date,
            daily_rate=reservation.days,
        )
        reservation.save()
        return Response({'status': 'Bron qabul qilindi'})


class BookRentViewSet(viewsets.ModelViewSet):
    queryset = BookRent.objects.all()
    http_method_names = ['get', 'post']
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsOperatorOrSuperAdmin(), ]
        return [IsAuthenticated(), ]

    def get_serializer_class(self):
        if self.action == 'create':
            return RentSerializer
        return BookRentSerializer

    def list(self, request, *args, **kwargs):
        if request.user.user_type == "Customer":
            rents = BookRent.objects.filter(user=request.user.id).all()
        elif request.user.user_type == "Operator" or request.user.is_superuser:
            rents = BookRent.objects.all()
        page = self.paginate_queryset(rents)
        if page is not None:
            serializer = self.get_paginated_response(BookRentSerializer(page, many=True).data)
        else:
            serializer = BookRentSerializer(rents, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        reservation = BookReservation.objects.filter(id=request.data['id']).first()
        if reservation.is_confirmed:
            return Response({"message": "Ushbu bron oldin tasdiqlangan"},
                            status=status.HTTP_200_OK)
        if not reservation:
            return Response({'message': "Bron topilmadi"},
                            status=status.HTTP_404_NOT_FOUND)
        rent = BookRent.objects.create(
            user=reservation.user,
            book=reservation.book,
            return_date=reservation.expiration_date,
            daily_rate=reservation.days,
        )
        reservation.is_confirmed = True
        reservation.save()
        return Response({"message": f"{reservation.user} mijozga {reservation.book} kitobi berildi"},
                        status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOperatorOrSuperAdmin, ],
            serializer_class=RentSerializer)
    def return_book(self, request, pk=None):
        book_rent = self.get_object()
        if book_rent.status == "Kitob qaytarilgan":
            return Response({"message": "Ushbu mijoz bu kitobni qaytarib bo'lgan"},
                            status=status.HTTP_200_OK)
        book_rent.return_date = timezone.now()
        book_rent.status = "Kitob qaytarilgan"
        book_rent.book.quantity += 1
        book_rent.rent_cost = book_rent.calculate_total_rent_cost()
        book_rent.finally_cost = book_rent.calculate_total_fine()
        book_rent.save()
        return Response({'status': f'{book_rent.user} mijoz {book_rent.book} kitobini qaytardi',
                         'total_rent_cost': book_rent.calculate_total_rent_cost(),
                         'total_fine': book_rent.calculate_total_fine()})


# class BookRentWithoutUser(viewsets.ModelViewSet):
#     queryset = BookRent.objects.exclude(rental_user__isnull=False).all()
#     permission_classes = [IsAuthenticated, IsOperatorOrSuperAdmin]
#     serializer_class = RentWithoutCustomer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             rental_user = RentalUser.objects.filter(id=serializer.validated_data['rental_user']).first()
#             if not rental_user:
#                 return Response({"message": "Bunday mijoz topilmadi"},
#                                 status=status.HTTP_404_NOT_FOUND)
#             book = Book.objects.filter(id=serializer.validated_data['book']).first()
#             daily_rate = serializer.validated_data['daily_rate']
#             return_date = timezone.now() + timezone.timedelta(days=daily_rate)
#             rent_book = BookRent.objects.create(rental_user=rental_user, book=book, daily_rate=daily_rate,
#                                                 return_date=return_date)
#             rent_book.save()
#             return Response(
#                 {
#                     "message": f"{rental_user.full_name} Ismi va {rental_user.phone_number} raqamli mijozga {book} kitobi berildi"})
