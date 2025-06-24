from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)  # in kg
    warranty = models.CharField(max_length=100, blank=True)

    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    # Consider using a separate model or ManyToMany for multiple images
    additional_images = models.ImageField(upload_to="product_images/additional/", blank=True, null=True)

    is_featured = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])
