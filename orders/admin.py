from django.contrib import admin
from orders.models import Company, CustomUser, Order, Product

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CustomUser)