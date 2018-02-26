from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    PROGRAMME_CHOICES = (
        ('B.Tech.', 'B.Tech.'),
        ('B.Des.', 'B.Des.'),
        ('M.Tech.', 'M.Tech.'),
        ('M.Des.', 'M.Des.'),
        ('PhD', 'PhD'),
    )

    DEPARTMENT_CHOICES = (
        ('CSE', 'CSE'),
        ('ME', 'ME'),
        ('ECE', 'ECE'),
        ('Design', 'Design'),
    )

    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    programme = models.CharField(max_length=10, choices=PROGRAMME_CHOICES)
    discipline = models.CharField(max_length=3, choices=DEPARTMENT_CHOICES)
    dob = models.DateField(blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)
    contact = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)
    is_contact_hidden = models.BooleanField(default=False)
    display_picture = models.ImageField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.programme, self.batch)


class Class(models.Model):
    name = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, related_name='student_class', on_delete=models.CASCADE)
    village = models.CharField(max_length=50, blank=True, null=True)
    sex = models.CharField(max_length=10, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    mother = models.CharField(max_length=50, blank=True, null=True)
    father = models.CharField(max_length=50, blank=True, null=True)
    contact = models.IntegerField(blank=True, null=True)
    emergency_contact = models.IntegerField(blank=True, null=True)
    display_picture = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self._class, self.village)


class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='user_attendance', on_delete=models.CASCADE)
    class_date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.class_date)


class Hobby(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class UserHobby(models.Model):
    user = models.ForeignKey(User, related_name='hobby_user', on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, related_name='user_hobby', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.hobby)


class Skill(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class UserSkill(models.Model):
    user = models.ForeignKey(User, related_name='skill_user', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='user_skill', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.user, self.skill)


class Subject(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class VolunteerSubject(models.Model):
    volunteer = models.ForeignKey(User, related_name='volunteer_subject', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subject_volunteer', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.volunteer, self.subject)


class Syllabus(models.Model):
    _class = models.ForeignKey(Class, related_name='class_syllabus', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subject_syllabus', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self._class, self.subject, self.content)


class StudentFeedback(models.Model):
    student = models.ForeignKey(User, related_name='student_feedback', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='volunteer_feedback', on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    feedback = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.student, self.user, self.title, self.feedback)


class ClassFeedback(models.Model):
    _class = models.ForeignKey(Class, related_name='class_feedback', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='subject_feedback', on_delete=models.CASCADE)
    feedback = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self._class, self.subject, self.feedback)


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ('EVENT', 'EVENT'),
        ('MEETING', 'MEETING')
    )

    time = models.DateTimeField()
    _type = models.CharField(max_length=7, choices=EVENT_TYPE_CHOICES)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.title, self.time, self._type)


class VolunteerClass(models.Model):
    volunteer = models.ForeignKey(User, related_name='volunteer_class', on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, related_name='class_volunteer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.volunteer, self._class)


class JoinRequest(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED')
    )

    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.email, self.name, self.status)
