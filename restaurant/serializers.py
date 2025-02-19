from rest_framework import serializers
from .models import Table, Section, Restaurant

class IikoOrderItemSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    sum = serializers.DecimalField(max_digits=10, decimal_places=2)
    deleted = serializers.BooleanField(required=False)

class IikoDiscountSerializer(serializers.Serializer):
    discountType = serializers.DictField()
    sum = serializers.DecimalField(max_digits=10, decimal_places=2)

class IikoWaiterSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField(required=False)

class IikoOrderSerializer(serializers.Serializer):
    id = serializers.CharField()
    externalNumber = serializers.CharField(required=False)
    tableIds = serializers.ListField(child=serializers.CharField())
    status = serializers.CharField()
    creationStatus = serializers.CharField()
    waiter = IikoWaiterSerializer(required=False)
    items = IikoOrderItemSerializer(many=True, required=False)
    discounts = IikoDiscountSerializer(many=True, required=False)
    sum = serializers.DecimalField(max_digits=10, decimal_places=2)

class IikoCallWaiterRequestSerializer(serializers.Serializer):
    department_id = serializers.CharField()
    table_number = serializers.CharField()
    waiter_id = serializers.CharField(required=False)

class RestaurantSerializer(serializers.ModelSerializer):
    sections_count = serializers.IntegerField(source='sections.count', read_only=True)
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'sections_count']

class SectionSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    tables_count = serializers.IntegerField(source='tables.count', read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'restaurant', 'restaurant_name', 'tables_count']
        
    def validate_name(self, value):
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Название секции должно содержать минимум 2 символа"
            )
        return value

class TableSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    restaurant_name = serializers.CharField(source='section.restaurant.name', read_only=True)
    uuid = serializers.UUIDField(required=False)
    qr_url = serializers.SerializerMethodField()

    class Meta:
        model = Table
        fields = [
            'uuid',
            'number',
            'section',
            'section_name',
            'restaurant_name',
            'qr',
            'qr_url',
            'call_waiter',
            'call_time',
            'bill_waiter', 
            'bill_time',
            'organization_id',
            'iiko_waiter_id',
            'iiko_department_id'
        ]
        read_only_fields = ['qr', 'qr_url', 'call_time', 'bill_time']

    def get_qr_url(self, obj):
        if obj.qr:
            return self.context['request'].build_absolute_uri(obj.qr.url)
        return None

    def validate_uuid(self, value):
        if value and Table.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("Этот UUID уже существует")
        return value

    def validate_number(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Номер стола должен быть положительным числом"
            )
        return value

    def validate(self, data):
        if 'section' in data and 'number' in data:
            exists_query = Table.objects.filter(
                section=data['section'],
                number=data['number']
            )
            if self.instance:
                exists_query = exists_query.exclude(pk=self.instance.pk)
            if exists_query.exists():
                raise serializers.ValidationError(
                    "Стол с таким номером уже существует в данной секции"
                )
        return data