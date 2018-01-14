from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Class
from .serializers import UserSerializer, ClassSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
