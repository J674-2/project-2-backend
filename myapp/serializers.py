from rest_framework import serializers
from .models import OrderItem, Order

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

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    class Meta:
        fields = ['id', 'date_time', 'order_items']
        model = Order
    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item in order_items:
            OrderItem.objects.create(order=order, **order_item)
        return order