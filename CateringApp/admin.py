from django.contrib import admin
from .models import Product_Category, Product_Master, Review, UserProfile, Order, Cart, ProductImage

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Product_Master)
admin.site.register(Product_Category)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(ProductImage)
admin.site.register(Review)

