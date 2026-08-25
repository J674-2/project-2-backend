from django.db import models

class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.date_time)

class OrderItem(models.Model):
    item = models.CharField(choices={'toast':'toast', 'salad':'salad', 'croquettes':'croquettes', 'spaghetti':'spaghetti', 'pie':'pie', 'burger':'burger','strawberries':'strawberries', 'ice cream':'ice cream', 'cookies':'cookies'}) 
    item_quantity = models.IntegerField()
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.item) + ', ' + str(self.order)