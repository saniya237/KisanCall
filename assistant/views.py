from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from twilio.twiml.voice_response import VoiceResponse

from .models import FarmerQuery
from .serializers import FarmerQuerySerializer

# ViewSet for internal dashboard or debugging
class FarmerQueryViewSet(viewsets.ModelViewSet):
    queryset = FarmerQuery.objects.all().order_by("-timestamp")
    serializer_class = FarmerQuerySerializer


@csrf_exempt
@api_view(["POST"])
def twilio_webhook(request):
    """
    Twilio voice call webhook implementation (Person 4 Task 3).
    Saves the incoming speech and plays back a response using TwiML.
    """
    # 1. Get SpeechResult and Phone Number from Twilio POST data
    # (Note: Use request.data here for DRF, or request.POST for standard Django)
    speech_result = request.data.get('SpeechResult', 'Empty Query')
    phone_number = request.data.get('From', 'Unknown')

    # 2. Simulated AI response (Task 3 focuses on connectivity)
    ai_response = "Your rice crop needs more water. Use NPK fertilizer."

    # 3. Prepare data and save via Serializer
    data = {
        'query_text': speech_result,
        'response_text': ai_response,
        'phone_number': phone_number
    }
    
    serializer = FarmerQuerySerializer(data=data)
    if serializer.is_valid():
        serializer.save()

    # 4. Generate TwiML to respond with voice
    twiml_response = VoiceResponse()
    twiml_response.say(ai_response)

    return HttpResponse(str(twiml_response), content_type='text/xml')


@api_view(["POST"])
def process_query(request):
    """Placeholder for manual API query processing."""
    query_text = request.data.get("query_text", "")
    phone = request.data.get("phone_number", "")
    
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


@api_view(["GET"])
def health_check(request):
    return Response({"status": "OK", "model": "FarmerQuery"})