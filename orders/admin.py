import csv
from django.contrib import admin
from django.http import HttpResponse
from orders.models import Company, CustomUser, Order, Product

admin.site.register(Company)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'price', 'stock', 'is_active']
    actions = ['mark_inactive','mark_active']

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected products as inactive"

    def mark_active(self,request,queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected products as active"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'company', 'status', 'created_at','shipped_at']
    actions = ['export_orders_csv']

    def export_orders_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Product', 'Quantity', 'Created By', 'Status', 'Created At'])
        for order in queryset:
            writer.writerow([
                order.id,
                order.product.name,
                order.quantity,
                order.created_by.username,
                order.status,
                order.created_at
            ])
        return response
    export_orders_csv.short_description = "Export selected orders as CSV"



admin.site.register(CustomUser)