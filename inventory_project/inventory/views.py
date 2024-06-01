from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema
from .serializers import AddItemSerializer, RemoveItemSerializer
from django.http import HttpResponse
from datetime import datetime
import csv
import os
from .application_service import (
    add_item_service,
    remove_item_service,
    get_stock_level_service,
    get_all_stock_levels_service,
    get_critical_notifications_service,
    export_history_service
)

@extend_schema(
    request=AddItemSerializer,
    responses={200: 'Item added successfully'}
)
@api_view(['POST'])
def add_item(request):
    serializer = AddItemSerializer(data=request.data)
    if serializer.is_valid():
        item_name = serializer.validated_data['item']
        quantity = serializer.validated_data['quantity']
        add_item_service(item_name, quantity)
        return Response({'status': 'item added'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=RemoveItemSerializer,
    responses={200: 'Item removed successfully'}
)
@api_view(['POST'])
def remove_item(request):
    serializer = RemoveItemSerializer(data=request.data)
    if serializer.is_valid():
        item_name = serializer.validated_data['item']
        quantity = serializer.validated_data['quantity']
        try:
            remove_item_service(item_name, quantity)
            return Response({'status': 'item removed'}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_stock_level(request, item_name):
    try:
        item = get_stock_level_service(item_name)
        return Response({"item": item.name, "quantity": item.quantity}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_all_stock_levels(request):
    items = get_all_stock_levels_service()
    return Response([{"item": item.name, "quantity": item.quantity} for item in items], status=status.HTTP_200_OK)

@api_view(['GET'])
def get_critical_notifications(request):
    critical_items = get_critical_notifications_service()
    return Response([{"item": item.name, "quantity": item.quantity} for item in critical_items], status=status.HTTP_200_OK)

@api_view(['GET'])
def export_history(request):
    history_data = export_history_service()

    filename = f"history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    file_path = f"inventory/history/reports/{filename}"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'w', newline='') as csvfile:
        file_writer = csv.writer(csvfile)
        file_writer.writerow(['Item', 'Quantity'])
        for row in history_data:
            file_writer.writerow([row['Item'], row['Quantity']])

    # Запись данных в HTTP-ответ
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow(['Item', 'Quantity'])
    for row in history_data:
        writer.writerow([row['Item'], row['Quantity']])

    return response
