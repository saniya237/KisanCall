from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"farmers",  views.FarmerViewSet)
router.register(r"sessions", views.CallSessionViewSet)
router.register(r"queries",  views.QueryLogViewSet)

urlpatterns = [
    path("session/start/", views.start_session),
    path("query/process/", views.process_query),
    path("health/", views.health_check),

    # 🎤 PERSON 3: Speech endpoints
    path("stt/", views.speech_to_text_view),
    path("tts/", views.text_to_speech_view),
]