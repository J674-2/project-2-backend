from rest_framework.test import APITestCase 
from rest_framework import status
from .models import Order, OrderItem
from django.test import tag, TestCase
import json

orders = [
    {'item': 'spaghetti', 'item_quantity': 2},
    {'item': 'burger', 'item_quantity': 1}, 
    {'item': 'salad', 'item_quantity': 4}, 
    {'item': 'pie', 'item_quantity': 3},
    {'item': 'ice cream', 'item_quantity': 5}
]

@tag('OrderList')
class OrderListTests(APITestCase):
    def test_get_no_orders(self):
        # Tests that the first page of orders is correctly returned, when there are no previous orders.
        response = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_get_first_page_orders(self):
        # Tests that the first page of orders is correctly returned, when there are previous orders.
        order_obj = Order.objects.create()
        OrderItem.objects.create(order=order_obj, item=orders[0]['item'], item_quantity=orders[0]['item_quantity'])
        response = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(
            str(response.data), 
            r"^{'count': 1, 'next': None, 'previous': None, 'results': \[{'id': 1, 'date_time': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z', 'order_items': \[{'id': 1, 'item': 'spaghetti', 'item_quantity': 2}\]}\]}$"
        )

    def test_get_second_page_orders(self):
        # Tests that the second page of orders is correctly returned, when there are previous orders. 
        for order in orders:
            order_obj = Order.objects.create()
            OrderItem.objects.create(order=order_obj, item=order['item'], item_quantity=order['item_quantity'])
        response = self.client.get('/api/orders', query_params={'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRegex(
            str(response.data), 
            r"^{'count': 5, 'next': None, 'previous': 'http://testserver/api/orders', 'results': \[{'id': 2, 'date_time': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z', 'order_items': \[{'id': 2, 'item': 'burger', 'item_quantity': 1}\]}, {'id': 1, 'date_time': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z', 'order_items': \[{'id': 1, 'item': 'spaghetti', 'item_quantity': 2}\]}\]}$"
        )

@tag('OrderCreate')
class OrderCreateTests(APITestCase):
    def test_no_order_created_when_order_items_field_missing(self):
        # Tests that an order is not created, when the order_items field is not included in the request.
        response_1 = self.client.post('/api/orders', data={}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': ['This field is required.']})
            
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_order_items_is_empty_array(self):
        # Tests that an order is not created, when the order_items field's value is an empty array.
        response_1 = self.client.post('/api/orders', data={'order_items': []}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': ['Order creation requires order items.']})
    
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_item_quantity_field_missing(self):
        # Tests that an order is not created, when the item_quantity field is not included in the request.
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item': 'spaghetti'}]}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': {'0': {'item_quantity': ['This field is required.']}}})
    
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_item_quantity_less_than_one(self):
        # Tests that an order is not created, when an item quantity has a value below one. 
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item': 'spaghetti', 'item_quantity': 0}]}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': {'0': {'item_quantity': ['Ensure this value is greater than or equal to 1.']}}})

        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_item_quantity_more_than_six(self):
        # Tests that an order is not created, when an item quantity has a value over six. 
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item': 'spaghetti', 'item_quantity': 7}]}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': {'0': {'item_quantity': ['Ensure this value is less than or equal to 6.']}}})
        
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_item_field_missing(self):
        # Tests that an order is not created, when the item field is not included in the request. 
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item_quantity': 5}]}, content_type='application/json') 
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': {'0': {'item': ['This field is required.']}}})
    
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_item_not_in_choices(self):
        # Tests that an order is not created, when an item is not one of the specified choices. 
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item': 'carrots', 'item_quantity': 5}]}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response_1.content), {'order_items': {'0': {'item': ['\"carrots\" is not a valid choice.']}}})
                
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_no_order_created_when_item_repeated(self):
        # Tests that an order is not created, when an item is repeated in the request's data. 
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item': 'spaghetti', 'item_quantity': 5}, {'item': 'spaghetti', 'item_quantity': 3}]}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_1.data, {'order_items': {'non_field_errors': ['Duplicate order items were found.']}})
                        
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_2.data, {'count': 0, 'next': None, 'previous': None, 'results': []})

    def test_order_created_when_data_valid(self):
        # Tests that an order is created, when the request's data is valid. 
        response_1 = self.client.post('/api/orders', data={'order_items': [{'item': 'spaghetti', 'item_quantity': 5}]}, content_type='application/json')
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        self.assertRegex(str(response_1.data), r"^{'id': 1, 'date_time': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z', 'order_items': \[{'id': 1, 'item': 'spaghetti', 'item_quantity': 5}\]}$")
                        
        response_2 = self.client.get('/api/orders', query_params={'page': 1})
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertRegex(str(response_2.data), r"^{'count': 1, 'next': None, 'previous': None, 'results': \[{'id': 1, 'date_time': '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{6}Z', 'order_items': \[{'id': 1, 'item': 'spaghetti', 'item_quantity': 5}\]}\]}$")

@tag('HealthCheck')
class HealthCheckTests(TestCase):
    def test_health_check_ok(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        