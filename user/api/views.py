from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password

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

    def update(self, request, *args, **kwargs):
        user = User.objects.filter(id=kwargs['pk']).first()
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


