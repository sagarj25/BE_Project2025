from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Product_Master)
admin.site.register(Product_Category)
admin.site.register(Cart)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Staff)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created', 'updated')  # Fields to display in the table
    list_filter = ('user', 'status')  # Fields to use for filtering
    search_fields = ('user', 'status')  # Fields to search in
    list_per_page = 20


