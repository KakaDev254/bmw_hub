from .models import Cart

def get_cart(request):
    """Return or create a cart for the authenticated user."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    return None
