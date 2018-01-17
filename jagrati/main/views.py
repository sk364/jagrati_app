from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Attendance, Class, UserClass, UserProfile
from .serializers import AttendanceSerializer, ClassSerializer, UserProfileSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @list_route(methods=['get'])
    def students(self, request):
        """
        Query Params:
          - `class_id` (integer, required)
        Response: list of user profiles
        """

        class_id = request.query_params.get('class_id', None)
        if class_id is not None:
            query = {
                'user__is_staff': False,
                'user__is_superuser': False,
                'user__class_user___class': class_id
            }
            queryset = UserProfile.objects.filter(**query)
            serializer = UserProfileSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response({
            'success': False,
            'detail': 'Required argument `class_id` missing.'
        }, status=status.HTTP_400_BAD_REQUEST)


class AttendaceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filter_fields = ('_class', 'class_date', )

    def create(self, request):
        """
        Request Data:
          - `class_id` (integer, required)
          - `student_ids` (string of comma-separated integers [eg: "1,2,3"], required)
        Response: dict
        """

        class_id = request.data.get('class_id', None)
        student_ids = request.data.get('student_ids', None)
        # class_date = request.data.get('class_date', None)
        class_attendance = []
        errors = ''

        if class_id is None or student_ids is None:
            return Response({
                'success': False,
                'detail': 'Missing Required Arguments.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            _class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return Response({
                'success': False,
                'detail': 'Class with id {} does not exist.'.format(class_id)
            }, status=status.HTTP_400_BAD_REQUEST)

        student_ids = student_ids.split(',')
        for student_id in student_ids:
            try:
                # check if user is in this class
                UserClass.objects.get(user=student_id, _class=_class)

                class_attendance.append(Attendance(
                    user=User.objects.get(id=student_id),
                    _class=_class
                ))
            except (User.DoesNotExist, UserClass.DoesNotExist):
                errors += student_id + ', '

        Attendance.objects.bulk_create(class_attendance)

        if errors is '':
            return Response({
                'success': True,
                'detail': 'Class Attendance Saved.'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'success': False,
                'detail': 'Unsaved student ids - {}'.format(errors)
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
