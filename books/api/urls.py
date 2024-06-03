from rest_framework.routers import DefaultRouter

from books.api.views import BookViewSet

book_router = DefaultRouter()
book_router.register('', BookViewSet, basename='books')

urlpatterns = book_router.urls
