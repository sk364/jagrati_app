import random
import string

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from .models import (Attendance, Class, ClassFeedback, Event, JoinRequest,
                     StudentFeedback, StudentProfile, Subject, Syllabus,
                     UserHobby, UserProfile, UserSkill, VolunteerSubject, )
from .permissions import IsAnonymousUserForPOST
from .serializers import (AttendanceSerializer, ClassSerializer,
                          ClassFeedbackSerializer, EventSerializer,
                          JoinRequestSerializer, StudentFeedbackSerializer,
                          StudentProfileSerializer, SubjectSerializer,
                          SyllabusSerializer, UserHobbySerializer,
                          UserProfileSerializer, UserSerializer,
                          UserSkillSerializer, VolunteerSubjectSerializer, )


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
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', )
    lookup_field = 'user__id'


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
    queryset = ClassFeedback.objects.all().order_by('-created_at')
    serializer_class = ClassFeedbackSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', )
    lookup_field = '_class__id'

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

    @detail_route(methods=['put'])
    def process(self, request, pk):
        """
        :desc: Processes the join request for approval/rejection
        :body: `type` Process Type (Choices: "A" or "R")
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

            if join_req_obj.status == 'PENDING':
                if process_type == 'A':
                    name = join_req_obj.name
                    email = join_req_obj.email

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
                    message = 'Sorry, we can\'t take you in our team.'
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
