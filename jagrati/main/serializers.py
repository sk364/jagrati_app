from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Attendance, Class


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_superuser', 'is_staff')


# TODO: Complete this.
class UserProfileSerializer(serializers.ModelSerializer):
    pass


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ('id', 'name', )


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())

    class Meta:
        model = Attendance
        fields = ('user', '_class', 'class_date', )
