from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Table, Section
from .serializers import TableSerializer, SectionSerializer, RestaurantSerializer
import uuid
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех секций",
        responses={200: SectionSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создать новый стол",
        request_body=TableSerializer,
        responses={201: TableSerializer()}
    )
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if 'uuid' not in data:
            data['uuid'] = uuid.uuid4()
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    @swagger_auto_schema(operation_description="Сгенерировать QR-код для стола")
    def generate_qr(self, request, pk=None):
        table = self.get_object()
        return Response({'status': 'QR код успешно сгенерирован'})
    
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Получить список всех ресторанов",
        responses={200: RestaurantSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Создать новый ресторан",
        request_body=RestaurantSerializer,
        responses={201: RestaurantSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class TableDetailView(DetailView):
    model = Table
    template_name = 'restaurant/table_detail.html'
    context_object_name = 'table'
    
    def get_object(self, queryset=None):
        return get_object_or_404(Table, uuid=self.kwargs.get('uuid'))