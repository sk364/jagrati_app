from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, ClassViewSet, EventViewSet, UserProfileViewSet,
                    AttendaceViewSet, StudentProfileViewSet, )

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'volunteers', UserProfileViewSet)
router.register(r'attendance', AttendaceViewSet)
router.register(r'students', StudentProfileViewSet)
router.register(r'events', EventViewSet)

urlpatterns = router.urls
