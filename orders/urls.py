from django.urls import path

from orders import views

urlpatterns = [
    path('',views.index,name='index'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),
]
