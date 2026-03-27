import uuid
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from twilio.twiml.voice_response import VoiceResponse

# ✅ ONLY USE FARMER QUERY (Single Model Architecture for Stable Demo)
from .models import FarmerQuery
from .serializers import FarmerQuerySerializer

# ✅ AI & SPEECH MODULES
from .ai_module import generate_response
from .speech import speech_to_text, text_to_speech


# -------------------------------
# 👨‍🌾 ADMIN/DASHBOARD VIEWSETS (Reused for Stability)
# -------------------------------
class FarmerViewSet(viewsets.ModelViewSet):
    queryset = FarmerQuery.objects.all().order_by("-timestamp")
    serializer_class = FarmerQuerySerializer

class CallSessionViewSet(viewsets.ModelViewSet):
    queryset = FarmerQuery.objects.all().order_by("-timestamp")
    serializer_class = FarmerQuerySerializer

class QueryLogViewSet(viewsets.ModelViewSet):
    queryset = FarmerQuery.objects.all().order_by("-timestamp")
    serializer_class = FarmerQuerySerializer

class FarmerQueryViewSet(viewsets.ModelViewSet):
    queryset = FarmerQuery.objects.all().order_by("-timestamp")
    serializer_class = FarmerQuerySerializer


# -------------------------------
# 🎤 PERSON 3: Speech to Text (STT)
# -------------------------------
@api_view(['POST'])
@parser_classes([MultiPartParser])
def speech_to_text_view(request):
    """Input: audio file ('audio'). Output: { 'text': 'transcription' }."""
    if 'audio' not in request.FILES:
        return Response({"error": "No audio file provided"}, status=400)

    audio_file = request.FILES['audio']
    text = speech_to_text(audio_file)

    return Response({"text": text})


# -------------------------------
# 🔊 PERSON 3: Text to Speech (TTS)
# -------------------------------
@api_view(['POST'])
def text_to_speech_view(request):
    """Input: { 'text': '...' }. Output: { 'audio_url': '...' }."""
    text = request.data.get("text", "")

    if not text:
        return Response({"error": "No text provided"}, status=400)

    audio_path = text_to_speech(text)

    return Response({"audio_url": f"/{audio_path}"})


# -------------------------------
# 📞 TWILIO WEBHOOK (Person 4 Logic)
# -------------------------------
@csrf_exempt
@api_view(["POST"])
def twilio_webhook(request):
    """Twilio voice call webhook. Saves speech and plays AI response."""
    speech_result = request.data.get('SpeechResult', 'Empty Query')
    phone_number = request.data.get('From', 'Unknown-Farmer')

    ai_response = "Your rice crop needs more water. Use NPK fertilizer soon."

    # Save to consolidated model
    FarmerQuery.objects.create(
        query_text=speech_result,
        response_text=ai_response,
        phone_number=phone_number,
        session_id=str(uuid.uuid4())[:8]
    )

    twiml_response = VoiceResponse()
    twiml_response.say(ai_response)

    return HttpResponse(str(twiml_response), content_type='text/xml')


# -------------------------------
# 🚀 START SESSION (Person 1 Logic)
# -------------------------------
@api_view(["POST"])
def start_session(request):
    """Initializes a new tracking session for a farmer."""
    phone = request.data.get("phone")

    if not phone:
        return Response({"error": "phone is required"}, status=400)

    new_session_id = str(uuid.uuid4())

    FarmerQuery.objects.create(
        phone_number=phone,
        session_id=new_session_id,
        query_text="SYSTEM_START",
        response_text="Session Initialized"
    )

    return Response({
        "session_id": new_session_id,
        "phone": phone,
        "status": "Session active"
    }, status=201)


# -------------------------------
# 🤖 PROCESS QUERY (MAIN AI API - Person 1)
# -------------------------------
@api_view(["POST"])
def process_query(request):
    """Primary API endpoint using the AI module for real-time responses."""
    session_id = request.data.get("session_id")
    user_query = request.data.get("user_query", "").strip()
    location = request.data.get("location", "Unknown Location")
    crop = request.data.get("crop", "Unknown Crop")

    if not session_id or not user_query:
        return Response({"error": "session_id and user_query required"}, status=400)

    # FIRE REAL AI ENGINE
    ai_response = generate_response(user_query, location, crop)

    # SAVE TO CONSOLIDATED MODEL
    FarmerQuery.objects.create(
        session_id=session_id,
        query_text=user_query,
        response_text=ai_response,
        location=location,
        crop=crop
    )

    return Response({
        "query": user_query,
        "response": ai_response,
        "session_id": session_id
    }, status=200)


# -------------------------------
# 📝 MANUAL QUERY (Person 4 Placeholder)
# -------------------------------
@api_view(["POST"])
def manual_query_process(request):
    query_text = request.data.get("query_text", "")
    phone = request.data.get("phone_number", "Unknown")
    
    if not query_text:
        return Response({"error": "query_text is required"}, status=400)

    ai_response = f"Simulated response to: {query_text}"

    query = FarmerQuery.objects.create(
        query_text=query_text,
        response_text=ai_response,
        phone_number=phone,
        location=request.data.get("location", ""),
        crop=request.data.get("crop", "")
    )

    return Response(FarmerQuerySerializer(query).data, status=201)


# -------------------------------
# ❤️ HEALTH CHECK
# -------------------------------
@api_view(["GET"])
def health_check(request):
    return Response({"status": "KisanCall AI Active (Person 1+3+4 Unlocked)"})