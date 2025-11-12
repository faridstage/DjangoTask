from django.db import models
from django.contrib.auth.models import AbstractUser 

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CustomUser(AbstractUser):
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    role = models.CharField(choices=[('viewer','Viewer'),('operator','Operator'),('admin','Admin')],max_length=20)

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('success','Success'),
        ('failed','Failed')
    ]
    company = models.ForeignKey(Company,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,max_length=20,default='pending')
    shipped_at = models.DateTimeField(null=True,blank=True)
