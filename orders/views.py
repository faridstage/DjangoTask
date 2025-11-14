from decimal import Decimal
import logging
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from orders.forms import OrderForm, ProductForm
from orders.models import Order, Product
from orders.serializers import OrderSerializer, ProductSerializer 
from rest_framework import status
import csv
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.authentication import SessionAuthentication

logger = logging.getLogger(__name__)

def ship_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, company=request.user.company)
    if order.shipped_at is None:
        order.shipped_at = timezone.now()
        order.status = 'success'
        order.save()
    return redirect('order_email_sim', order_id=order.id)

def order_email_sim(request, order_id):
    order = get_object_or_404(Order, id=order_id, company=request.user.company)
    return render(request, 'orders/order_email_sim.html', {'order': order})

def addOrder(request):
    form = OrderForm(user= request.user)
    return render(request,'orders/addOrder.html',{'form':form})


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
    
def order_list_page(request):
    orders = Order.objects.filter(company=request.user.company)
    return render(request, 'orders/listOrders.html', {'orders': orders})


class OrderListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get(self, request):
        orders = Order.objects.filter(company=request.user.company)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
class OrderAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from orders.services import create_orders
        try:
            created_ids = create_orders(request.user, request.data.get("orders", []))
            return Response({"created_orders": created_ids})
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)

    
class ProductSoftDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        from orders.services import soft_delete_products
        ids = request.data.get("product_ids", [])
        deleted = soft_delete_products(request.user, ids)
        return Response({"deleted_ids": deleted})


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


class EditProductsByOperatorsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        from orders.services import edit_product
        try:
            product = edit_product(
                request.user,
                request.data.get("product_id"),
                request.data.get("name"),
                request.data.get("price"),
                request.data.get("stock"),
            )
            return Response({"message": "Product updated successfully"})
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
