from rest_framework import serializers

from orders.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'is_active', 'created_by', 'created_at', 'last_updated_at']
        read_only_fields = ['created_by', 'created_at', 'last_updated_at']