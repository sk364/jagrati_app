from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ClassViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'classes', ClassViewSet)

urlpatterns = router.urls
