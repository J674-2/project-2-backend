from django.db import models

class Order(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.date_time)
