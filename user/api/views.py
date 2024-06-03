from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication

from user.api.permissions import IsSuperAdmin, IsAdminOrOwner
from user.api.serializers import UserSerializer
from user.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'put']
    authentication_classes = (JWTAuthentication, SessionAuthentication)

    def get_permissions(self):
        if self.action == 'list':
            return [IsSuperAdmin(), ]
        if self.action == 'create':
            return [AllowAny(),]
        return [IsAdminOrOwner()]


