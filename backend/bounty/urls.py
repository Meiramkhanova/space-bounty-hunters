from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HuntLogViewSet, WantedCriminalViewSet

router = DefaultRouter()
router.register("criminals", WantedCriminalViewSet, basename="criminal")
router.register("hunts", HuntLogViewSet, basename="hunt")

urlpatterns = [
    path("", include(router.urls)),
]
