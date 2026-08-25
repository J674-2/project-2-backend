from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView
from .models import Order
from .serializers import OrderSerializer

def health_check_view(request):
    return HttpResponse(status=200)

class OrderView(ListCreateAPIView):
    queryset = Order.objects.prefetch_related('order_items').order_by('-id')
    serializer_class = OrderSerializer