from rest_framework import serializers

from orders.models import CustomUser, Product

from axes.handlers.proxy import AxesProxyHandler


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock', 'is_active', 'created_by', 'created_at', 'last_updated_at']
        read_only_fields = ['created_by', 'created_at', 'last_updated_at']

class UserSerializer(serializers.ModelSerializer):
    
    is_blocked = serializers.SerializerMethodField()

    def get_is_blocked(self,obj):
        request = self.context['request']
        return AxesProxyHandler.is_locked(request,{'username':obj})
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'last_login',
            'is_staff',
            'is_active',
            'role',
            'company_id'
            'is_blocked'
        ]