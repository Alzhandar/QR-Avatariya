import os
import uuid
import logging
import requests
from datetime import datetime, timedelta

from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Table, Section
from .serializers import *
from .services import IikoService, IikoWaiterService

logger = logging.getLogger(__name__)


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

        if table.organization_id:
            iiko_service = IikoService()
            iiko_service.ensure_token_in_redis()

        context.update({
            'whatsapp_url': os.getenv('WHATSAPP_URL'),
            'instagram_url': os.getenv('INSTAGRAM_URL'),
            'FeedbackForm': os.getenv('FEEDBACK'),
            'restaurant_name': table.section.restaurant.name if table.section else "Avatariya",
            'section_name': table.section.name if table.section else "Основной зал",
            'table_number': table.number,
            'timestamp': timezone.now().strftime("%Y-%m-%d %H:%M:%S")
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
    template_name = 'restaurant/check.html'
    context_object_name = 'table'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_object()

        if not table:
            context['error'] = "Стол не найден"
            return context

        if not table.organization_id:
            context['error'] = "ID организации не указан для данного стола"
            return context

        try:
            iiko_service = IikoService()
            order_data = iiko_service.get_token_and_order_by_table(
                organization_id=table.organization_id,
                table_uuid=str(table.uuid)
            )
            print(order_data)

            if not order_data or 'orders' not in order_data:
                context['order_found'] = False
                context['message'] = "Данные о заказе не найдены"
                return context

            active_order = next(
                (o for o in order_data['orders']
                 if o['creationStatus'] == 'Success'),
                None
            )
            if not active_order:
                context['order_found'] = False
                context['message'] = "Заказ не найден или уже закрыт"
                return context

            order = active_order['order']
            context['order_info'] = {
                'id': active_order['id'],
                'number': order.get('number'),
                'created': order.get('whenCreated'),
                'source': order.get('sourceKey', 'Неизвестно'),
                'status': order.get('status')
            }
            

            customer = order.get('customer', {})
            context['customer'] = {
                'name': customer.get('name', 'Гость'),
                'phone': order.get('phone'),
                'guests_count': order.get('guestsInfo', {}).get('count', 1)
            }

            context['waiter'] = order.get('waiter', {})

            items = []
            for item in order.get('items', []):
                if not item.get('deleted'):
                    items.append({
                        'name': item['product']['name'],
                        'amount': item['amount'],
                        'price': float(item.get('price', 0)),
                        'cost': float(item.get('cost', 0)),
                        'result_sum': float(item.get('resultSum', 0)),
                        'status': item.get('status')
                        
                    })
            context['items'] = items
            context['order_found'] = True

        except ValueError as e:
            logger.error(f"Ошибка валидации при запросе iiko: {e}")
            context['error'] = str(e)
        except Exception as e:
            logger.error(f"Ошибка при запросе iiko для стола {table.number}: {str(e)}")
            context['error'] = str(e)

        return context


class CallWaiterView(DetailView):
    model = Table
    template_name = 'restaurant/call-waiter.html'
    context_object_name = 'table'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = self.get_object()
        iiko_service = IikoService()

        try:
            order_data = iiko_service.get_token_and_order_by_table(
                organization_id=str(table.organization_id),
                table_uuid=str(table.uuid)
            )
            
            orders = order_data.get('orders', [])
            active_order = next((o for o in orders if o['creationStatus'] == 'Success'), None)

            if active_order:
                order = active_order.get('order', {})
                waiter = order.get('waiter', {})
                context.update({
                    'has_active_order': True,
                    'waiter': {
                        'name': waiter.get('name'),
                        'id': waiter.get('id')
                    },
                    'order_number': order.get('number')
                })
                logger.info(f"Информация об официанте: {waiter}")
            else:
                context.update({
                    'has_active_order': False
                })
                logger.info("У стола нет активного заказа")

        except Exception as e:
            logger.error(f"Ошибка при получении данных: {e}")
            context.update({
                'has_active_order': False,
                # 'error_message': "Ошибка при получении данных об официанте"
            })

        return context
    
    def post(self, request, *args, **kwargs):
        table = self.get_object()
        iiko_service = IikoService()
        iiko_waiter_service = IikoWaiterService()

        try:
            if not table.organization_id:
                raise ValueError("У этого стола не указаны данные об организации")

            logger.info(f"Запрос данных для стола №{table.number}")
            
            order_data = iiko_service.get_token_and_order_by_table(
                organization_id=str(table.organization_id),
                table_uuid=str(table.uuid)
            )
            
            orders = order_data.get('orders', [])
            active_order = next((o for o in orders if o['creationStatus'] == 'Success'), None)

            if active_order:
                logger.info(f"Статус стола №{table.number}: Есть активный заказ")
                order = active_order.get('order', {})
                waiter = order.get('waiter', {})
                logger.info(f"Информация о заказе:")
                logger.info(f"- Номер заказа: {order.get('number')}")
                logger.info(f"- Официант: {waiter.get('name', 'Не назначен')}")
                logger.info(f"- ID официанта: {waiter.get('id', 'Не указан')}")
                
                iiko_waiter_service.call_waiter(
                    department_id=str(table.section_id),
                    table_number=str(table.number),
                    user_id=waiter.get('id')
                )
                success_message = "Вызов официанта выполнен успешно."
            else:
                logger.info(f"Статус стола №{table.number}: Нет активного заказа")
                new_order_id = str(uuid.uuid4())
                logger.info(f"Создаем новый заказ с ID: {new_order_id}")
                
                iiko_waiter_service.broadcast_new_order(
                    order_id=new_order_id,
                    table_number=str(table.number)
                )
                success_message = "Выполнен broadcast на создание нового заказа. Официант уведомлён."

            return render(request, self.template_name, {
                'table': table,
                'success_message': success_message
            })
        except Exception as e:
            error_message = f"Ошибка при вызове официанта: {str(e)}"
            logger.error(error_message)
            return render(request, self.template_name, {
                'table': table,
                'error_message': error_message
            })