import jwt
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_decode_handler

from .models import (Attendance, Class, ClassFeedback, Event, StudentProfile, Subject,
                     Syllabus, UserHobby, UserProfile, UserSkill, )
from .serializers import (AttendanceSerializer, ClassSerializer, ClassFeedbackSerializer,
                          EventSerializer, StudentProfileSerializer, SyllabusSerializer,
                          UserHobbySerializer, UserProfileSerializer, UserSerializer,
                          UserSkillSerializer, )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class VolunteerProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user__id'

    def get_queryset(self):
        return UserProfile.objects.filter(user__is_staff=True)


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    lookup_field = 'user__id'


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


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UserHobbyViewSet(viewsets.ModelViewSet):
    queryset = UserHobby.objects.all()
    serializer_class = UserHobbySerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('user', 'hobby', )


class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('user', 'skill', )


class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', )


class ClassFeedbackViewSet(viewsets.ModelViewSet):
    queryset = ClassFeedback.objects.all()
    serializer_class = ClassFeedbackSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', )

    def create(self, request):
        data = request.data
        _class = data.get('_class', None)
        subject = data.get('subject', None)
        feedback = data.get('feedback', None)
        is_invalid_data = True

        if _class is not None and subject is not None and feedback is not None:
            is_invalid_data = False
            _class_id = _class.get('id', None)
            subject_id = subject.get('id', None)

            if _class_id is not None and subject_id is not None:
                try:
                    Class.objects.get(id=_class_id)
                except Class.DoesNotExist:
                    is_invalid_data = True

                try:
                    Subject.objects.get(id=subject_id)
                except Subject.DoesNotExist:
                    is_invalid_data = True

                if is_invalid_data is False:
                    return super(ClassFeedbackViewSet, self).create(request)

            is_invalid_data = True

        if is_invalid_data:
            return Response({
                'success': False,
                'detail': 'Data is invalid'
            }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    def get(self, request):
        """
        :desc: GET HTTP request handler to process jwt
        """

        _jwt = request.query_params.get('jwt', None)

        if _jwt is None:
            return Response({
                'success': False,
                'detail': 'Missing jwt query param'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = jwt_decode_handler(_jwt)
        except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError):
            return Response({
                'detail': 'Token is invalid',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)

        user_id = payload['user_id']
        user = User.objects.get(id=user_id)
        is_admin = user.is_superuser

        return Response({
            'user_id': user_id,
            'is_admin': is_admin,
            'success': True
        })
