from django.urls import path, include

from .custom_jwt_claims import CustomTokenObtainPairView

from rest_framework.routers import DefaultRouter


from orders import views

urlpatterns = [
    path('',views.index,name='index'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),
    path('api/orders/', views.OrderAPIView.as_view(), name='api_orders'),
    path('api/products/delete/', views.ProductSoftDeleteAPIView.as_view(), name='api_products_delete'),
    path('api/orders/export/', views.OrderExportToCSVAPIView.as_view(), name='api_orders_export'),
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair')
]
