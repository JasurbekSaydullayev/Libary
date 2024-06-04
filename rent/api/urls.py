from django.urls import path
from rest_framework.routers import DefaultRouter

from books.api.views import BookViewSet
from .views import BookReservationViewSet, BookRentViewSet

router = DefaultRouter()
router.register('reservations', BookReservationViewSet, basename='reservations')
router.register('rents', BookRentViewSet, basename='rents')

urlpatterns = router.urls

urlpatterns += [
    path('reservations/<int:pk>/cancel/', BookReservationViewSet.as_view({'post': 'cancel'}),
         name='cancel-reservation'),
    path('reservations/<int:pk>/confirm/', BookReservationViewSet.as_view({'post': 'confirm'}),
         name='confirm-reservation'),
    # path('rents/<int:pk>/return/', BookRentViewSet.as_view({'post': 'return_book'}), name='return-book'),
]
