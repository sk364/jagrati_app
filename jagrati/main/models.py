from __future__ import unicode_literals

import datetime

from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    contact = models.BigIntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=128, blank=True, null=True)
    is_contact_hidden = models.BooleanField(default=False)
    display_picture = models.ImageField(upload_to='uploads/', blank=True, null=True)
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
    contact = models.BigIntegerField(blank=True, null=True)
    emergency_contact = models.BigIntegerField(blank=True, null=True)
    display_picture = models.ImageField(upload_to='uploads/', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self._class, self.village)


class Attendance(models.Model):
    user = models.ForeignKey(User, related_name='user_attendance', on_delete=models.CASCADE)
    class_date = models.DateField(default=datetime.date.today)
    is_extra_class = models.BooleanField(default=False)
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

    class Meta:
        unique_together = ('volunteer', 'subject')

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

    class Meta:
        ordering = ('-created_at', )

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

    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return '{} - {} - {}'.format(self.email, self.name, self.status)


class Notification(models.Model):
    to_only_admin = models.BooleanField(default=True)
    _type = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    display_date = models.DateTimeField(default=datetime.datetime.now)
    instance_id = models.IntegerField(default=-1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {} - {}'.format(self._type, self.content, self.created_at)


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.notification, self.is_seen)


class Config(models.Model):
    num_inactive_student_days = models.IntegerField(default=7)

    def __str__(self):
        return 'Inactive Student Days: {}'.format(self.num_inactive_student_days)


def create_notification(obj, _type, content, to_only_admin, instance_id):
    """
    :desc: Creates a notification object.
    :param: `obj` Model instance
    """

    # display when the event will happen rather than when event was created
    created_at = obj.created_at if _type != 'event' else obj.time

    notification = Notification.objects.create(
        _type=_type,
        content=content,
        to_only_admin=to_only_admin,
        display_date=obj.created_at,
        instance_id=instance_id
    )

    if to_only_admin:
        filters = {'is_superuser': True}
    else:
        filters = {'is_staff': True}

    users = User.objects.filter(**filters)
    user_notifications = [UserNotification.objects.create(user=user, notification=notification)
                          for user in users]


@receiver(post_save, sender=JoinRequest)
def send_join_request_mail(sender, instance, **kwargs):
    created = kwargs.get('created', False)

    if created:
        create_notification(instance, 'join_request', instance.name, True, instance.id)
        subject = 'New Join Request!'
        message = 'New Join Request by {email}'.format(email=instance.email)
        from_email = 'support@jagrati.com'
        to_email = [settings.EMAIL_HOST_USER]

        send_mail(subject, message, from_email, to_email, fail_silently=False)


@receiver(post_save, sender=Event)
def create_event_notification(sender, instance, **kwargs):
    create_notification(instance, 'event', instance.title, False, instance.id)

@receiver(post_save, sender=ClassFeedback)
def create_class_feedback_notification(sender, instance, **kwargs):
    create_notification(instance, 'class_feedback', instance._class.name, False, instance._class.id)
