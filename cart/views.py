from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += int(request.POST.get('quantity', 1))
    else:
        item.quantity = int(request.POST.get('quantity', 1))
    item.save()

    messages.success(request, f"{product.name} added to cart.")
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if item.cart.user == request.user:
        item.delete()
        messages.success(request, "Item removed from cart.")
    return redirect('view_cart')

def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
    
    if request.method == "POST":
        new_quantity = int(request.POST.get("quantity", 1))
        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, f"Updated quantity for {item.product.name}.")
        else:
            item.delete()
            messages.info(request, f"{item.product.name} removed from cart.")
    return redirect("view_cart")

def ajax_update_cart(request, item_id):
    if request.method == 'POST' and request.is_ajax():
        item = get_object_or_404(CartItem, id=item_id, cart=request.user.cart)
        new_quantity = int(request.POST.get("quantity", 1))

        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            return JsonResponse({
                'status': 'success',
                'subtotal': float(item.get_subtotal()),
                'total': float(request.user.cart.get_total()),
                'message': f"Updated quantity for {item.product.name}."
            })
        else:
            item.delete()
            return JsonResponse({
                'status': 'removed',
                'total': float(request.user.cart.get_total()),
                'message': f"Removed {item.product.name} from cart."
            })

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

