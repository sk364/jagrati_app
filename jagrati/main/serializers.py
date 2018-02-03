from __future__ import unicode_literals

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (Attendance, Class, StudentProfile, UserProfile,
                     Hobby, UserHobby, Skill, UserSkill, Subject,
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
    class Meta:
        model = Class
        fields = ('id', 'name', )


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())
    _class = ClassSerializer(Class.objects.all())

    class Meta:
        model = StudentProfile
        fields = ('user', '_class', 'village', 'sex', 'dob', 'mother', 'father',
                  'contact', 'emergency_contact', 'display_picture', )


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserSerializer(User.objects.all())
    _class = ClassSerializer(Class.objects.all())

    def get_photo_url(self, obj):
        dp = obj.user.user_profile.display_picture
        return dp.url if dp else ''

    photo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = ('user', '_class', 'class_date', 'photo_url')


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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'time', '_type', 'title', 'description', 'image', )
