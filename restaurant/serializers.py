from rest_framework import serializers
from .models import Table, Section, Restaurant

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False)
    class Meta:
        model = Table
        fields = ('uuid', 'number', 'section', 'iiko_guid')
        read_only_fields = ('qr',)

    def validate_uuid(self, value):
        if value and Table.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("Этот UUID уже существует")
        return value
    
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'