from django.urls import path, include

from .custom_jwt_claims import CustomTokenObtainPairView

from rest_framework.routers import DefaultRouter


from orders import views

urlpatterns = [
    path('',views.index,name='index'),
    path('add',views.addOrder,name='add'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),
    path('api/orders/', views.OrderAPIView.as_view(), name='api_orders'),
    path('list/', views.order_list_page, name='order_list_page_view'),
    path('ship/<int:order_id>/', views.ship_order, name='ship_order'),
    path('email/<int:order_id>/', views.order_email_sim, name='order_email_sim'),
    path('api/orders/list/', views.OrderListAPIView.as_view(), name='api_orders_list'),
    path('api/products/delete/', views.ProductSoftDeleteAPIView.as_view(), name='api_products_delete'),
    path('api/orders/export/', views.OrderExportToCSVAPIView.as_view(), name='api_orders_export'),
    path('api/products/edit/',views.EditProductsByOperatorsAPIView.as_view(),name='api_edit_products'),
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair')
]
