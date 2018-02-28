from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import (AttendaceViewSet, ClassViewSet, ClassFeedbackViewSet,
                    JoinRequestViewSet, EventViewSet, StudentFeedbackViewSet,
                    StudentProfileViewSet, SubjectViewSet, SyllabusViewSet,
                    UserHobbyViewSet, UserSkillViewSet, UserViewSet,
                    VolunteerProfileViewSet, VolunteerSubjectViewSet, )

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'volunteers', VolunteerProfileViewSet)
router.register(r'attendance', AttendaceViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'events', EventViewSet)
router.register(r'user_hobbies', UserHobbyViewSet)
router.register(r'user_skills', UserSkillViewSet)
router.register(r'syllabus', SyllabusViewSet)
router.register(r'class_feedback', ClassFeedbackViewSet)
router.register(r'student_feedback', StudentFeedbackViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'department', VolunteerSubjectViewSet)
router.register(r'join_requests', JoinRequestViewSet)

urlpatterns = router.urls
