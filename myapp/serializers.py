from rest_framework import serializers
from .models import OrderItem

class CustomListSerializer(serializers.ListSerializer):
    def validate(self, data):
        items_list = []
        for dict in data:
            items_list.append(dict['item'])
        if len(items_list) != len(set(items_list)):
            raise serializers.ValidationError('Duplicate order items were found.')
        return data

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'item', 'item_quantity']
        model = OrderItem
        list_serializer_class = CustomListSerializer
        extra_kwargs = {'item_quantity':{'min_value': 1, 'max_value': 6}}