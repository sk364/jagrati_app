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

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.programme, self.batch)


class Class(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return '{} - {}'.format(self.id, self.name)


class UserClass(models.Model):
    user = models.ForeignKey(User, related_name='class_user', on_delete=models.CASCADE)
    _class = models.ForeignKey(Class, related_name='user_class', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.user, self._class)


class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='user_attendance', on_delete=models.CASCADE) 
    _class = models.ForeignKey(Class, related_name='class_attendance', on_delete=models.CASCADE)
    class_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self._class, self.class_date)
