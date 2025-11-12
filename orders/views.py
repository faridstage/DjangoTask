from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from orders.forms import ProductForm
from orders.models import Product
from orders.serializers import ProductSerializer 

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
        
    products = Product.objects.filter(company=request.user.company)
    return render(request,'orders/index.html',{'form':form,'products':products})

class ProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(company=request.user.company, is_active=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)