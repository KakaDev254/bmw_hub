from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# View Cart Page
@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})


# Add Product to Cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('view_cart')


# Remove Item from Cart
@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('view_cart')


# Update Quantity in Cart (Standard POST)
@login_required
def update_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == "POST":
        try:
            new_quantity = int(request.POST.get("quantity", 1))
            if new_quantity > 0:
                item.quantity = new_quantity
                item.save()
                messages.success(request, f"Updated quantity for {item.product.name}.")
            else:
                item.delete()
                messages.info(request, f"{item.product.name} removed from cart.")
        except (ValueError, TypeError):
            messages.error(request, "Invalid quantity.")
    
    return redirect("view_cart")


# Update Quantity via AJAX
@login_required
def ajax_update_cart(request, item_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart = get_object_or_404(Cart, user=request.user)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        try:
            new_quantity = int(request.POST.get("quantity", 1))
            if new_quantity > 0:
                item.quantity = new_quantity
                item.save()
                return JsonResponse({
                    'status': 'success',
                    'subtotal': float(item.get_subtotal()),
                    'total': float(cart.get_total()),
                    'message': f"Updated quantity for {item.product.name}."
                })
            else:
                item.delete()
                return JsonResponse({
                    'status': 'removed',
                    'total': float(cart.get_total()),
                    'message': f"Removed {item.product.name} from cart."
                })
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid quantity.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})
