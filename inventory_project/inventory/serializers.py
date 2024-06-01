# inventory/serializers.py
from rest_framework import serializers

class AddItemSerializer(serializers.Serializer):
    item = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField(min_value=1)

class RemoveItemSerializer(serializers.Serializer):
    item = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField(min_value=1)