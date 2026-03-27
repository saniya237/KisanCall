from rest_framework import serializers
from .models import FarmerQuery

class FarmerQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerQuery
        fields = "__all__"

    def create(self, validated_data):
        return FarmerQuery.objects.create(**validated_data)