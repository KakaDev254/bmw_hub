from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    featured_products = Product.objects.filter(is_featured=True, in_stock=True)[:6]
    latest_products = Product.objects.filter(in_stock=True).order_by('-created_at')[:6]
    categories = Category.objects.all()

    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'categories':categories,
        
    })


def shop_view(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(in_stock=True)

    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }
    return render(request, 'products/shop.html', context)
    
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {'product': product})    
