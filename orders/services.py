from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError
from orders.models import Order, Product
from decimal import Decimal


def create_orders(user, orders_data):
    if user.role == "viewer":
        raise ValidationError("Viewer can't order!")

    created_order_ids = []

    for data in orders_data:
        product_id = data.get("product_id")
        quantity = data.get("quantity")

        try:
            product = Product.objects.get(id=product_id, company=user.company)
        except Product.DoesNotExist:
            raise ValidationError(f"Product {product_id} does not exist")
        
        if not product.is_active:
            raise ValidationError(f"Product '{product.name}' is not active")
        
        if quantity > product.stock:
            raise ValidationError("Not enough stock available")
        

        product.stock -= quantity
        product.save()


        order = Order.objects.create(
            company=user.company,
            product=product,
            quantity=quantity,
            created_by=user,
            status="pending",
        )

        created_order_ids.append(order.id)

    return created_order_ids



def edit_product(user, product_id, name, price, stock):
    if user.role == "viewer":
        raise ValidationError("Only Operators and Admins can edit")


    now = timezone.now()
    limit = now - timedelta(hours=24)

    try:
        product = Product.objects.get(id=product_id, company=user.company, created_at__gte=limit)
    except Product.DoesNotExist:
        raise ValidationError("You can only edit products created within last 24 hours")

    if name:
        product.name = name

    if price is not None:
        product.price = Decimal(price)

    if stock is not None:
        product.stock = stock

    product.save()

    return product



def soft_delete_products(user, ids):
    products = Product.objects.filter(id__in=ids, company=user.company)
    products.update(is_active=False)
    return ids
