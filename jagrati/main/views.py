from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Attendance, Class, StudentProfile, UserProfile
from .serializers import (AttendanceSerializer, ClassSerializer,
                          StudentProfileSerializer, UserProfileSerializer,
                          UserSerializer, )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class AttendaceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', 'class_date', )

    def get_attendance_objs(self, student_ids):
        """
        Params:
          - `student_ids` list of student IDs
        Returns a tuple of list of Attendance objects and errors
        """

        attendance_objs = []
        errors = []
        for student_id in student_ids:
            try:
                attendance_objs.append(Attendance(
                    user=User.objects.get(id=student_id)
                ))
            except User.DoesNotExist:
                errors.append(student_id)

        return attendance_objs, errors


    def create(self, request):
        """
        Request Data:
          - `student_ids` (list of integers [eg: [1,2,3]], required)
        Response: dict
        """

        student_ids = request.data.get('student_ids', None)
        # class_date = request.data.get('class_date', None)

        if student_ids is None:
            return Response({
                'success': False,
                'detail': 'Missing Required Arguments.'
            }, status=status.HTTP_400_BAD_REQUEST)


        attendance_objs, errors = self.get_attendance_objs(student_ids)

        if attendance_objs:
            Attendance.objects.bulk_create(attendance_objs)

        if errors == []:
            return Response({
                'success': True,
                'detail': 'Class Attendance Saved.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'detail': 'Unsaved student ids - {}'.format(', '.join(errors))
            }, status=status.HTTP_201_CREATED)


    @list_route(methods=['get'])
    def class_dates(self, request):
        """
        Query Params:
          - `class_id` (integer, required)
        Response: list of dates
        """

        class_id = request.query_params.get('class_id', None)

        if class_id is None:
            return Response({
                'success': False,
                'detail': 'Missing required arguments.'
            }, status=status.HTTP_400_BAD_REQUEST)

        attendance_dates = Attendance.objects.filter(
            _class=class_id
        ).values_list('class_date', flat=True).distinct()

        return Response({
            'success': True,
            'dates': attendance_dates
        })
