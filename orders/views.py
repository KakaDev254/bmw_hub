from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.utils import get_cart
from .models import Order, OrderItem
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart = get_cart(request)
    if cart.is_empty():
        return redirect('shop')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
            cart.clear()
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

def order_success(request, order_id):
    return render(request, 'orders/success.html', {'order_id': order_id})
