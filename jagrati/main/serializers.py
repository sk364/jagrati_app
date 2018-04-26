from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from .models import (Attendance, Class, ClassFeedback, Event, Hobby, JoinRequest,
                     Notification, Skill, StudentFeedback, StudentProfile, Subject,
                     Syllabus, UserHobby, UserNotification, UserProfile, UserSkill,
                     VolunteerSubject, )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'is_superuser', 'is_staff')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.filter(is_staff=True, is_superuser=False), read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.filter(is_staff=True, is_superuser=False),
        write_only=True
    )

    def get_attendance(self, obj):
        """
        :desc: Computes class attendance of user
        :param: `obj` Model instance
        :return: attendance information `dict`
        """

        user_attendance = obj.user.user_attendance.count()
        total_classes = Attendance.objects.values('class_date').distinct().count()

        return {
            'attendance': user_attendance,
            'total_classes': total_classes
        }

    attendance = serializers.SerializerMethodField(read_only=True)

    def get_hobbies(self, obj):
        hobbies = []

        for hobby_user in obj.user.hobby_user.all():
            hobbies.append({
                'id': hobby_user.hobby.id,
                'name': hobby_user.hobby.name
            })

        return hobbies

    hobbies = serializers.SerializerMethodField(read_only=True)

    def get_skills(self, obj):
        skills = []

        for skill_user in obj.user.skill_user.all():
            skills.append({
                'id': skill_user.skill.id,
                'name': skill_user.skill.name
            })

        return skills

    skills = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'user_id', 'programme', 'discipline', 'dob', 'batch', 'contact',
                  'address', 'status', 'is_contact_hidden', 'display_picture', 'attendance',
                  'hobbies', 'skills', )


class ClassSerializer(serializers.ModelSerializer):
    def get_num_active_students(self, obj):
        """
        :desc: Computes number of active students in a class.
        :param: `obj` Model instance
        :return: Count of active students
        """

        return StudentProfile.objects.filter(
            user__is_active=True,
            _class=obj
        ).count()

    num_active_students = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Class
        fields = ('id', 'name', 'num_active_students', 'updated_at', )


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.filter(is_staff=False, is_superuser=False), read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source='user',
        queryset=User.objects.filter(is_staff=False, is_superuser=False),
        write_only=True
    )
    _class = ClassSerializer(Class.objects.all(), read_only=True)
    _class_id = serializers.PrimaryKeyRelatedField(
        source='_class',
        queryset=Class.objects.all(),
        write_only=True
    )

    def get_attendance(self, obj):
        """
        :desc: Computes class attendance of user
        :param: `obj` Model instance
        :return: attendance information `dict`
        """

        user_attendance = obj.user.user_attendance.values('class_date').distinct().count()
        total_classes = Attendance.objects.values('class_date').distinct().count()

        return {
            'attendance': user_attendance,
            'total_classes': total_classes
        }

    attendance = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ('user', 'user_id', '_class', '_class_id', 'village', 'sex', 'dob', 'mother', 'father',
                  'contact', 'emergency_contact', 'display_picture', 'attendance', 'address', )


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all(), read_only=True)
    student_ids = serializers.ListField(
        child = serializers.PrimaryKeyRelatedField(
            queryset=User.objects.filter(is_staff=False, is_superuser=False),
            write_only=True
        ),
        write_only=True
    )

    def create(self, validated_data):
        students = validated_data['student_ids']
        attendance_objs = []

        for student in students:
            attendance_objs.append(self.Meta.model(user=student))

        self.Meta.model.objects.bulk_create(attendance_objs)
        return attendance_objs[0]

    class Meta:
        model = Attendance
        fields = ('user', 'class_date', 'student_ids', )
        read_only_fields = ('user', 'class_date', )


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ('id', 'name', )


class UserHobbySerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all(), read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    hobby = HobbySerializer(Hobby.objects.all(), read_only=True)
    hobby_id = serializers.PrimaryKeyRelatedField(
        queryset=Hobby.objects.all(),
        source='hobby',
        write_only=True
    )

    class Meta:
        model = UserHobby
        fields = ('user', 'user_id', 'hobby', 'hobby_id', )


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', )


class UserSkillSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all(), read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    skill = SkillSerializer(Skill.objects.all(), read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(
        queryset=Skill.objects.all(),
        source='skill',
        write_only=True
    )

    class Meta:
        model = UserSkill
        fields = ('user', 'user_id', 'skill', 'skill_id', )


class SubjectSerializer(serializers.ModelSerializer):
    def get_num_volunteers(self, obj):
        """
        :desc: Computes number of volunteers teaching a subject.
        """

        return VolunteerSubject.objects.filter(subject=obj).count()

    num_volunteers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'num_volunteers', )


class SyllabusSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(Class.objects.all(), read_only=True)
    _class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='_class',
        write_only=True
    )
    subject = SubjectSerializer(Subject.objects.all(), read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )

    class Meta:
        model = Syllabus
        fields = ('_class', '_class_id', 'subject', 'subject_id', 'content', )


class StudentFeedbackSerializer(serializers.ModelSerializer):
    student = UserSerializer(User.objects.filter(is_staff=False, is_superuser=False), read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=False, is_superuser=False),
        source='student',
        write_only=True
    )

    user = UserSerializer(User.objects.filter(Q(Q(is_staff=True) | Q(is_superuser=True))), read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(Q(Q(is_staff=True) | Q(is_superuser=True))),
        source='user',
        write_only=True
    )

    class Meta:
        model = StudentFeedback
        fields = ('student', 'student_id', 'user', 'user_id', 'title', 'feedback', )


class ClassFeedbackSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(Class.objects.all(), read_only=True)
    _class_id = serializers.PrimaryKeyRelatedField(
        queryset=Class.objects.all(),
        source='_class',
        write_only=True
    )
    subject = SubjectSerializer(Subject.objects.all(), read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )

    class Meta:
        model = ClassFeedback
        fields = ('_class', '_class_id', 'subject', 'subject_id', 'feedback', 'created_at', )


class VolunteerSubjectSerializer(serializers.ModelSerializer):
    volunteer = UserSerializer(User.objects.filter(is_staff=True, is_superuser=False), read_only=True)
    volunteer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True, is_superuser=False),
        source='volunteer',
        write_only=True
    )
    subject = SubjectSerializer(Subject.objects.all(), read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        source='subject',
        write_only=True
    )

    def get_discipline(self, obj):
        if obj.volunteer.user_profile:
            return obj.volunteer.user_profile.discipline
        return ''

    discipline = serializers.SerializerMethodField(read_only=True)

    def get_display_picture(self, obj):
        if obj.volunteer.user_profile and obj.volunteer.user_profile.display_picture:
            return obj.volunteer.user_profile.display_picture.url
        return ''

    display_picture = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = VolunteerSubject
        fields = ('volunteer', 'volunteer_id', 'subject', 'subject_id', 'discipline', 'display_picture', )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time', '_type', 'title', 'description', 'image', 'created_at', )


class JoinRequestSerializer(serializers.ModelSerializer):
    def validate(self, data):
        super().validate(data)
        email = data['email']

        try:
            user = User.objects.get(username=email)
            raise serializers.ValidationError("User with {} already exists".format(email))
        except User.DoesNotExist:
            return data

    class Meta:
        model = JoinRequest
        fields = ('id', 'email', 'name', 'status', 'created_at', )
        read_only_fields = ('status', )


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', '_type', 'content', 'instance_id', 'display_date', )


class UserNotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all(), read_only=True)
    notification = NotificationSerializer(Notification.objects.all(), read_only=True)

    class Meta:
        model = UserNotification
        fields = ('user', 'notification', 'is_seen')
