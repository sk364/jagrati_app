from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Attendance, Class, ClassFeedback, StudentProfile,
                     UserProfile, Hobby, UserHobby, Skill, UserSkill, Subject,
                     Syllabus, StudentFeedback, Event, )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_superuser', 'is_staff')


# TODO: Add `attendance_count` to `fields`
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'programme', 'discipline', 'dob', 'batch', 'contact',
                  'address', 'status', 'is_contact_hidden', 'display_picture', )


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
        fields = ('id', 'name', 'num_active_students', )


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())
    _class = ClassSerializer(Class.objects.all())

    def get_attendance_data(self, obj):
        """
        :desc: Computes class attendance
        :param: `obj` Model instance
        :return: attendance information `dict`
        """

        user_attendance = obj.user.user_attendance.count()
        total_classes = Attendance.objects.values('class_date').distinct().count()

        return {
            'attendance': user_attendance,
            'total_classes': total_classes
        }

    attendance_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ('user', '_class', 'village', 'sex', 'dob', 'mother', 'father',
                  'contact', 'emergency_contact', 'display_picture', 'attendance_data', )


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())
    _class = ClassSerializer(Class.objects.all())

    class Meta:
        model = Attendance
        fields = ('user', 'class_date', )


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ('id', 'name', )


class UserHobbySerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())
    hobby = HobbySerializer(Hobby.objects.all())

    class Meta:
        model = UserHobby
        fields = ('user', 'hobby', )


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', )


class UserSkillSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())
    skill = SkillSerializer(Skill.objects.all())

    class Meta:
        model = UserSkill
        fields = ('user', 'skill', )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', )


class SyllabusSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(Class.objects.all())
    subject = SubjectSerializer(Subject.objects.all())

    class Meta:
        model = Syllabus
        fields = ('_class', 'subject', 'content', )


class StudentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentFeedback
        fields = ('student', 'user', 'title', 'feedback', )


class ClassFeedbackSerializer(serializers.ModelSerializer):
    _class = ClassSerializer(Class.objects.all())
    subject = SubjectSerializer(Subject.objects.all())

    def create(self, validated_data):
        validated_data = self.initial_data
        class_id = validated_data['_class']['id']
        subject_id = validated_data['subject']['id']
        feedback = validated_data['feedback']

        class_feedback_obj = self.Meta.model.objects.create(
            _class_id=class_id, subject_id=subject_id, feedback=feedback
        )

        return class_feedback_obj

    class Meta:
        model = ClassFeedback
        fields = ('_class', 'subject', 'feedback', 'created_at', )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time', '_type', 'title', 'description', 'image', )
