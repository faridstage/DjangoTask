from django import forms
from .models import Order, Product


class ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = ['name', 'price', 'stock']

class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),
        label="Product",
        empty_label="Select a product"
    )
    quantity = forms.IntegerField(min_value=1, label="Quantity")

    class Meta:
        model = Order
        fields = ['product', 'quantity']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['product'].queryset = Product.objects.filter(company=user.company, is_active=True)