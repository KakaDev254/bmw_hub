from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('shop/', views.shop_view, name='shop'),
    path('shop/category/<slug:category_slug>/', views.shop_view, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]