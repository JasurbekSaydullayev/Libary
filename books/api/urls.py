from django.urls import path
from rest_framework.routers import DefaultRouter

from books.api.views import BookViewSet, RateBookAPIView

router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')

urlpatterns = [
    path('rate-book/', RateBookAPIView.as_view(), name='rate-book'),
]

urlpatterns += router.urls
