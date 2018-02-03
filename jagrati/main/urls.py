from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, ClassViewSet, EventViewSet, VolunteerProfileViewSet,
                    AttendaceViewSet, StudentProfileViewSet, UserDetailAPIView,
                    UserHobbyViewSet, UserSkillViewSet, )

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'volunteers', VolunteerProfileViewSet)
router.register(r'attendance', AttendaceViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'events', EventViewSet)
router.register(r'user_hobbies', UserHobbyViewSet)
router.register(r'user_skills', UserSkillViewSet)

urlpatterns = [
    url(r'user_details', UserDetailAPIView.as_view()),
] + router.urls
