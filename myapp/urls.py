from django.urls import path
from .views import health_check_view, OrderView

urlpatterns = [
    path('health', health_check_view),
    path('orders', OrderView.as_view()),
]