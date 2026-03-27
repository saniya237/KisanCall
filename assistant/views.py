from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
import uuid

from .models import Farmer, CallSession, QueryLog
from .serializers import FarmerSerializer, CallSessionSerializer, QueryLogSerializer
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# 🔥 SIMPLE TEST (NO AI FOR NOW)

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all().order_by("-created_at")
    serializer_class = FarmerSerializer


class CallSessionViewSet(viewsets.ModelViewSet):
    queryset = CallSession.objects.all().order_by("-started_at")
    serializer_class = CallSessionSerializer


class QueryLogViewSet(viewsets.ModelViewSet):
    queryset = QueryLog.objects.all().order_by("-timestamp")
    serializer_class = QueryLogSerializer


@api_view(["POST"])
def process_query(request):
    session_id = request.data.get("session_id")
    user_query = request.data.get("user_query", "").strip()

    if not session_id or not user_query:
        return Response({"error": "session_id and user_query required"}, status=400)

    try:
        session = CallSession.objects.get(session_id=session_id)
    except CallSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

    # --- AI Integration ---
@api_view(["POST"])
def process_query(request):
    session_id = request.data.get("session_id")
    user_query = request.data.get("user_query", "").strip()

    if not session_id or not user_query:
        return Response({"error": "session_id and user_query required"}, status=400)

    try:
        session = CallSession.objects.get(session_id=session_id)
    except CallSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)

    
    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_query
    )

    ai_response = response.output[0].content[0].text
    return Response({
        "query": user_query,
        "response": ai_response
    })
    

    log = QueryLog.objects.create(
        session=session,
        user_query=user_query,
        ai_response=ai_response
    )

    return Response(QueryLogSerializer(log).data, status=201)
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


@api_view(["GET"])
def health_check(request):
    return Response({"status": "OK"})