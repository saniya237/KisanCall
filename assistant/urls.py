from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"queries", views.FarmerQueryViewSet)

urlpatterns = [
    # Router endpoints
    path("", include(router.urls)),

    # Main Interaction Endpoints (Person 1 + 4)
    path("process/", views.process_query),
    path("start-session/", views.start_session),
    path("manual-query/", views.manual_query_process),
    path("health/", views.health_check),
    
    # Twilio Voice Webhook (Person 4)
    path("twilio-webhook/", views.twilio_webhook),

    # Speech Endpoints (Person 3)
    path("stt/", views.speech_to_text_view),
    path("tts/", views.text_to_speech_view),
]