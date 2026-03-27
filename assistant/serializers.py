from rest_framework import serializers
from .models import Farmer, CallSession, QueryLog


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Farmer
        fields = "__all__"


class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = QueryLog
        fields = "__all__"


class CallSessionSerializer(serializers.ModelSerializer):
    queries = QueryLogSerializer(many=True, read_only=True)

    class Meta:
        model  = CallSession
        fields = "__all__"