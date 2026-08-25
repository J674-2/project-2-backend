from rest_framework import serializers

class CustomListSerializer(serializers.ListSerializer):
    def validate(self, data):
        items_list = []
        for dict in data:
            items_list.append(dict['item'])
        if len(items_list) != len(set(items_list)):
            raise serializers.ValidationError('Duplicate order items were found.')
        return data