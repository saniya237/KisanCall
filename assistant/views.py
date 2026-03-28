import os
import uuid
from django.utils import timezone

from rest_framework import viewsets, status
<<<<<<< HEAD
from rest_framework.decorators import api_view
=======
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
>>>>>>> b1788def89e5fb92edb391e3664f31f272250731
from rest_framework.response import Response

from .models import Farmer, CallSession, QueryLog
from .serializers import FarmerSerializer, CallSessionSerializer, QueryLogSerializer
<<<<<<< HEAD

# ✅ IMPORT YOUR AI
from .ai_module import generate_response


=======
from .ai_module import generate_response
from .speech import speech_to_text, text_to_speech


>>>>>>> b1788def89e5fb92edb391e3664f31f272250731
# -------------------------------
# 👨‍🌾 FARMER APIs
# -------------------------------
class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all().order_by("-created_at")
    serializer_class = FarmerSerializer


# -------------------------------
# 📞 CALL SESSION APIs
# -------------------------------
class CallSessionViewSet(viewsets.ModelViewSet):
    queryset = CallSession.objects.all().order_by("-started_at")
    serializer_class = CallSessionSerializer


# -------------------------------
# 📊 QUERY LOG APIs
# -------------------------------
class QueryLogViewSet(viewsets.ModelViewSet):
    queryset = QueryLog.objects.all().order_by("-timestamp")
    serializer_class = QueryLogSerializer


# -------------------------------
<<<<<<< HEAD
=======
# 🎤 PERSON 3: Speech to Text
# -------------------------------
@api_view(['POST'])
@parser_classes([MultiPartParser])
def speech_to_text_view(request):
    """
    POST /api/stt/
    Input: audio file (form-data, key = 'audio')
    Output: { "text": "transcribed farmer query" }
    """
    if 'audio' not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)

    audio_file = request.FILES['audio']
    text = speech_to_text(audio_file)

    return Response({"text": text})


# -------------------------------
# 🔊 PERSON 3: Text to Speech
# -------------------------------
@api_view(['POST'])
def text_to_speech_view(request):
    """
    POST /api/tts/
    Input: { "text": "your response here" }
    Output: { "audio_url": "/media/response_xyz.mp3" }
    """
    text = request.data.get("text", "")

    if not text:
        return Response({"error": "No text provided"}, status=400)

    audio_path = text_to_speech(text)

    return Response({"audio_url": f"/{audio_path}"})


# -------------------------------
>>>>>>> b1788def89e5fb92edb391e3664f31f272250731
# 🚀 START SESSION
# -------------------------------
@api_view(["POST"])
def start_session(request):
    phone = request.data.get("phone")

    if not phone:
        return Response({"error": "phone is required"}, status=400)

    try:
        farmer = Farmer.objects.get(phone=phone)
    except Farmer.DoesNotExist:
        return Response({"error": "Farmer not found"}, status=404)

    session = CallSession.objects.create(
        farmer=farmer,
        session_id=str(uuid.uuid4()),
        status="active"
    )

    return Response(CallSessionSerializer(session).data, status=201)


# -------------------------------
# 🤖 PROCESS QUERY (MAIN AI API)
# -------------------------------
@api_view(["POST"])
def process_query(request):
    session_id = request.data.get("session_id")
    user_query = request.data.get("user_query", "").strip()
    location = request.data.get("location")
    crop = request.data.get("crop")

    if not session_id or not user_query:
        return Response({"error": "session_id and user_query required"}, status=400)

    try:
        session = CallSession.objects.get(session_id=session_id)
    except CallSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

<<<<<<< HEAD
    # 🔥 CALL YOUR AI MODULE (IMPORTANT)
    ai_response = generate_response(user_query, location, crop)

    # 💾 SAVE TO DATABASE
=======
    ai_response = generate_response(user_query, location, crop)

>>>>>>> b1788def89e5fb92edb391e3664f31f272250731
    log = QueryLog.objects.create(
        session=session,
        user_query=user_query,
        ai_response=ai_response
    )

    return Response({
        "query": user_query,
        "response": ai_response
    }, status=200)


# -------------------------------
# ❤️ HEALTH CHECK
# -------------------------------
@api_view(["GET"])
def health_check(request):
    return Response({"status": "OK"})