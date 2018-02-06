from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, ClassViewSet, ClassFeedbackViewSet, EventViewSet,
                    VolunteerProfileViewSet, AttendaceViewSet, StudentProfileViewSet,
                    SyllabusViewSet, UserDetailAPIView, UserHobbyViewSet, UserSkillViewSet, )

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

urlpatterns = [
    url(r'user_details', UserDetailAPIView.as_view()),
] + router.urls
