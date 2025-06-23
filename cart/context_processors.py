from .models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = sum(item.quantity for item in cart.items.all())
            total_price = cart.get_total()
        except Cart.DoesNotExist:
            total_items = 0
            total_price = 0
    else:
        total_items = 0
        total_price = 0

    return {
        'cart_item_count': total_items,
        'cart_total_price': total_price,
    }
