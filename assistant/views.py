from rest_framework import viewsets, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.utils import timezone
import uuid
import os

from .models import Farmer, CallSession, QueryLog
from .serializers import FarmerSerializer, CallSessionSerializer, QueryLogSerializer
from openai import OpenAI
from .speech import speech_to_text, text_to_speech

client = OpenAI(api_key=os.getenv("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"))

# 🔥 SIMPLE TEST (NO AI FOR NOW)

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all().order_by("-created_at")
    serializer_class = FarmerSerializer


# 🎤 PERSON 3: Speech to Text
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


# 🔊 PERSON 3: Text to Speech
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