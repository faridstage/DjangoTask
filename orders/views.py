import logging
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from orders.forms import ProductForm
from orders.models import Order, Product
from orders.serializers import ProductSerializer 
from rest_framework import status
import csv
from django.http import HttpResponse
from datetime import datetime
from django.contrib import admin

logger = logging.getLogger(__name__)



def index(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.company = request.user.company
            product.created_by =request.user
            product.save()
            return redirect('index')
    else:
        form = ProductForm()
        
    products = Product.objects.filter(company=request.user.company, is_active=True)
    return render(request,'orders/index.html',{'form':form,'products':products})

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(company=request.user.company, is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class OrderAPIView(APIView):
    permission_classes= [IsAuthenticated]

    def post(self,request):
        if request.user.role == 'viewer':
            return Response({"error":"Viewer Can't order!!"},status=status.HTTP_403_FORBIDDEN)
        
        orders_data = request.data.get('orders',[])
        created_orders = []
        for data in orders_data:
            try:
                product = Product.objects.get(id=data['product_id'], company=request.user.company)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with id {data['product_id']} does not exist or is unavailable"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not product.is_active:
                return Response(
                    {"error": f"This product '{product.name}' is currently unavailable"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            quantity = data['quantity']
            if quantity > product.stock:
                return Response({"error":"there is no enough of this product"},status=status.HTTP_400_BAD_REQUEST)
            product.stock -= quantity
            product.save()

            order = Order.objects.create(
                company = request.user.company,
                product=product,
                quantity = quantity,
                created_by = request.user,
                status = 'pending'
            )
            created_orders.append(order.id)
        
        return Response({"created_orders":created_orders})
    
class ProductSoftDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        ids = request.data.get('product_ids',[])
        products = Product.objects.filter(id__in=ids,company=request.user.company)
        products.update(is_active=False)
        return Response({"deleted_ids":ids})
    
class OrderExportToCSVAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        orders = Order.objects.filter(company=request.user.company)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="orders_{datetime.now().strftime("%Y%m%d")}.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Product', 'Quantity', 'Created By', 'Status', 'Created At'])
        for order in orders:
            writer.writerow([order.id, order.product.name, order.quantity, order.created_by.username, order.status, order.created_at])
        
        return response
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'price', 'stock', 'is_active']
    actions = ['mark_inactive']

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected products as inactive"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'company', 'status', 'created_at']
    
    actions = ['export_orders_csv']

    def export_orders_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Product', 'Quantity', 'Created By', 'Status', 'Created At'])
        for order in queryset:
            writer.writerow([order.id, order.product.name, order.quantity, order.created_by.username, order.status, order.created_at])
        return response
    export_orders_csv.short_description = "Export selected orders as CSV"