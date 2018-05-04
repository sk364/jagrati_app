import random
import string

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (Attendance, Class, ClassFeedback, Event, JoinRequest,
                     Notification, StudentFeedback, StudentProfile, Subject,
                     Syllabus, UserHobby, UserNotification, UserProfile,
                     UserSkill, VolunteerSubject, )
from .permissions import IsAnonymousUserForPOST, IsOwner
from .serializers import (AttendanceSerializer, ClassSerializer,
                          ClassFeedbackSerializer, EventSerializer,
                          JoinRequestSerializer, NotificationSerializer,
                          StudentFeedbackSerializer, StudentProfileSerializer,
                          SubjectSerializer, SyllabusSerializer,
                          UserHobbySerializer, UserNotificationSerializer,
                          UserProfileSerializer, UserSerializer,
                          UserSkillSerializer, VolunteerSubjectSerializer, )

DEFAULT_REJECTION_MSG = 'Sorry, we can\'t take you in our team.'


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
    permission_classes = (IsAuthenticated, IsOwner, )
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('user__is_active', )

    def get_queryset(self):
        return UserProfile.objects.filter(user__is_staff=True)

    def create(self, request):
        data = request.data
        user_id = data.get('user_id')

        if user_id is not None:
            user_profile = UserProfile.objects.filter(user_id=user_id).first()
            if user_profile is None:
                if request.user.id == user_id:
                    return super(VolunteerProfileViewSet, self).create(request)
            else:
                return Response({
                    'success': False,
                    'detail': 'You already have a profile.'
                })
        return Response({
            'success': False,
            'detail': 'You do not have permission to perform this action.'
        })


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', )
    lookup_field = 'user__id'

    def create(self, request, *args, **kwargs):
        data = dict(request.data)
        for key in data:
            value = list(data[key])[0]
            if value == '':
                value = None
            data[key] = value

        if data.get("first_name") and data.get('class_num'):
            first_name = data['first_name']
            last_name = data['last_name'] if data['last_name'] is not None else ''
            user = User.objects.create(username=first_name, first_name=first_name, last_name=last_name)

            class_num = data['class_num']
            _class = Class.objects.get(name=class_num)

            data['_class_id'] = _class.id
            data['user_id'] = user.id

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'message': 'Required fields - first_name/class_num not present.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = dict(request.data)
        for key in data:
            value = list(data[key])[0]
            if value == '':
                value = None

            data[key] = value

        if data.get('class_num'):
            instance = self.get_object()

            data['user_id'] = instance.user.id
            class_num = data['class_num']
            _class = Class.objects.filter(name=class_num).first()
            if _class:
                data['_class_id'] = _class.id
            else:
                return Response({
                    'success': False,
                    'message': 'Class does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(instance, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        else:
            return Response({
                'success': False,
                'message': 'Required fields - first_name/class_num not present.'
            }, status=status.HTTP_400_BAD_REQUEST)


class AttendaceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('class_date', )

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


class EventFilterSet(filters.FilterSet):
    created_at__gt = filters.IsoDateTimeFilter(name='created_at', lookup_expr='gt')

    class Meta:
        model = Event
        fields = ('created_at__gt', )


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_class = EventFilterSet


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
    queryset = ClassFeedback.objects.all().order_by('-created_at')
    serializer_class = ClassFeedbackSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', )
    lookup_field = '_class__id'


class StudentFeedbackViewSet(viewsets.ModelViewSet):
    queryset = StudentFeedback.objects.all()
    serializer_class = StudentFeedbackSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class VolunteerSubjectViewSet(viewsets.ModelViewSet):
    queryset = VolunteerSubject.objects.all()
    serializer_class = VolunteerSubjectSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('subject', 'volunteer', )


class JoinRequestViewSet(viewsets.ModelViewSet):
    queryset = JoinRequest.objects.all()
    serializer_class = JoinRequestSerializer
    permission_classes = (IsAnonymousUserForPOST, )
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('status', )

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email in User.objects.all().values_list('username', flat=True):
            return Response({
                'success': False,
                'detail': 'A user already exists with this email id.'
            })

        return super().create(request, *args, **kwargs)

    @detail_route(methods=['put'])
    def process(self, request, pk):
        """
        :desc: Processes the join request for approval/rejection
        :body: `type` Process Type (Choices: "A" or "R")
               `message` Rejection message
        """

        process_type = request.data.get('type')

        if process_type:
            try:
                join_req_obj = JoinRequest.objects.get(id=pk)
            except JoinRequest.DoesNotExist:
                return Response({
                    'success': False,
                    'detail': 'Invalid Join Request id.'
                }, status=status.HTTP_400_BAD_REQUEST)

            name = join_req_obj.name
            email = join_req_obj.email

            if join_req_obj.status == 'PENDING':
                if process_type == 'A':
                    if email in User.objects.all().values_list('username', flat=True):
                        return Response({
                            'success': False,
                            'detail': 'User with email already exists.'
                        }, status=status.HTTP_400_BAD_REQUEST)

                    user = User.objects.create(
                        username=email,
                        first_name=name,
                        last_name=name
                    )
                    password = self.get_random_password()
                    user.set_password(password)
                    user.save()

                    # send mail with password
                    subject = 'Welcome To Jagrati !'
                    message = 'Here are your account details - \n\
                               Username: {username}\n\
                               Password: {password}'.format(username=email, password=password)
                    from_email = 'support@jagrati.com'
                    to_email = [email]
                    send_mail(
                        subject,
                        message,
                        from_email,
                        to_email,
                        fail_silently=False
                    )

                    join_req_obj.status = 'APPROVED'
                    join_req_obj.save()
                elif process_type == 'R':
                    # send mail for rejection
                    subject = 'Message from Jagrati !'
                    message = request.data.get('message') or DEFAULT_REJECTION_MSG
                    from_email = 'support@jagrati.com'
                    to_email = [email]
                    send_mail(
                        subject,
                        message,
                        from_email,
                        to_email,
                        fail_silently=False
                    )

                    join_req_obj.status = 'REJECTED'
                    join_req_obj.save()
                else:
                    return Response({
                        'succes': False,
                        'detail': 'Invalid value for paramter `type`.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'detail': 'Already processed'
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'success': True,
                'detail': 'Successfully updated.'
            })
        else:
            return Response({
                'success': False,
                'detail': 'Missing `type` parameter.'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_random_password(self, password_len=8):
        return ''.join(
            random.SystemRandom().choice(string.ascii_letters + string.digits)
            for _ in range(password_len)
        )


class UserNotificationViewSet(viewsets.ModelViewSet):
    queryset = UserNotification.objects.all()
    serializer_class = UserNotificationSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('is_seen', )

    def get_queryset(self):
        return UserNotification.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        queryset = self.get_queryset()
        queryset.update(is_seen=True)
        return response
