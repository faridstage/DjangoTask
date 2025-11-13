from decimal import Decimal
import logging
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
    authentication_classes = [SessionAuthentication]

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


class EditProductsByOperatorsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request):
        if request.user.role == 'viewer':
            return Response({"error":"Only Operators and admins can edit this"}, status=status.HTTP_403_FORBIDDEN)

        now = datetime.now(timezone.utc)
        time_limit = now - timedelta(hours=24)

        editable_products = Product.objects.filter(company = request.user.company,created_at__gte=time_limit)

        product_id = request.data.get('product_id')
        new_name = request.data.get('name')
        new_price = Decimal(request.data.get('price'))
        new_stock = request.data.get('stock')

        try:
            product = editable_products.get(id=product_id)
        except:
            return Response({"error","you can only edit products that are created within 1 day"},status=status.HTTP_400_BAD_REQUEST)
        
        if new_name:
            product.name = new_name
        if new_price:
            product.price - new_price
        if new_stock:
            product.stock = new_stock

        product.save()

        return Response({"message":"Product updated successfully"},status=status.HTTP_200_OK)


