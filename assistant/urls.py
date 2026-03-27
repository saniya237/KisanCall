from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"queries", views.FarmerQueryViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("process/", views.process_query),
    path("health/", views.health_check),
    path("twilio-webhook/", views.twilio_webhook),  # New endpoint for Twilio calls
]