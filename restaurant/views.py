from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from .models import Table, Section
from .serializers import TableSerializer, SectionSerializer, RestaurantSerializer
import uuid
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, render
import os
from django.http import Http404
from django.utils import timezone


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
    template_name = 'restaurant/main.html'
    context_object_name = 'table'
    slug_field = 'uuid' 
    slug_url_kwarg = 'uuid'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_object()
        context.update({
            'whatsapp_url': os.getenv('WHATSAPP_URL'),
            'instagram_url': os.getenv('INSTAGRAM_URL'),
            'FeedbackForm': os.getenv('FEEDBACK'),
            'restaurant_name': table.section.restaurant.name if table.section else "Avatariya",
            'section_name': table.section.name if table.section else "Основной зал",
            'table_number': table.number
        })
        return context
    
class MenuChoiceView(DetailView):
    model = Table
    template_name = 'restaurant/menu.html'
    context_object_name = 'table'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'menu_ru': os.getenv('MENU_RU_URL'),
            'menu_kz': os.getenv('MENU_KZ_URL')
        })
        return context
    

class CSRFFailureView(View):
    template_name = 'restaurant/404_error.html'
    
    def get(self, request, reason=""):
        context = {
            'error_message': 'Ошибка проверки CSRF токена. Пожалуйста, попробуйте снова.',
            'status_code': 403,
            'reason': reason
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context,
            status=403
        )
    
    def post(self, request, reason=""):
        return self.get(request, reason)


class Error404View(View):
    template_name = 'restaurant/404_error.html'
    
    def get(self, request, exception=None):
        context = {
            'error_message': str(exception) if exception else 'Запрашиваемая страница не найдена',
            'status_code': 404,
        }
        return render(
            request=request,
            template_name=self.template_name,
            context=context,
            status=404
        )
    
    def post(self, request, exception=None):
        return self.get(request, exception)



class PredCheckView(DetailView):
    model = Table
    template_name = 'restaurant/pred_check.html'
    context_object_name = 'table'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_object()
        
        context.update({
            'table': table.number,
            'hall': table.section.name if table.section else "Основной зал",
            'num_zakaz': "A-" + str(table.number) + "-" + timezone.now().strftime("%Y%m%d"),
            'date': timezone.now(),
            'total': "15000", 
            'client': "Гость",
        })
        return context