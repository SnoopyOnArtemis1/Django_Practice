from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=220)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return super().__str__()   
    
class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField(blank=True)
    salesman = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now) #原本：()內是auto_now_add=True #add 'editable=False' if you don't want the users to edit date in the admin
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super(Purchase, self).save(*args,**kwargs)

    def __str__(self):
        return "Sold {} {} with a total of NT${}".format( self.quantity, self.product.name, self.total_price)
    


