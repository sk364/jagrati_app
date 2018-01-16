from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ClassViewSet, UserProfileViewSet, AttendaceViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'attendance', AttendaceViewSet)

urlpatterns = router.urls
