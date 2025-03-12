from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
USERSTATUS = ((1, "Active"), (2, "Inactive"))
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(choices=USERSTATUS, default=1, null=True, blank=True) 
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    image  = models.FileField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
class Product_Category(models.Model):
    name=  models.CharField(max_length=100, null=False, blank=False)
    image = models.FileField(upload_to='product/', null=True)
    createdby=models.CharField(max_length=100, null=False, blank=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
class Product_Master(models.Model):
    category = models.ForeignKey(Product_Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    price=models.FloatField(null=True, blank=True, default=0)
    desc=models.TextField(null=True, blank=True)
    detaildesc=models.TextField(null=True, blank=True)
    image=models.FileField(null=True, blank=True)
    createdby=models.CharField(max_length=100, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True, blank=True)
    updated=models.DateTimeField(auto_now=True, blank=True)
    active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def incrementprice(self):
        return self.price + (105/100)
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product_Master, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='product/', null=True,)
    
    def __str__(self):
        return self.product.name
    
class ProductHistory(models.Model):
    productid = models.CharField(max_length=100, null=True, blank=True)
    productcategoryid = models.CharField(max_length=100, null=True, blank=True)
    user = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.productid
    
ORDERSTATUS = ((1, "Confirmation"), (2, "Processing"), (3, "Preparing"), (4, "Ready"), (5, "Completion"), (6, "Cancel"), (7, "Refund")) 
class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    orderid = models.CharField(max_length =100, null=True, blank=True)
    productid = models.TextField(max_length =100, null=True, blank=True)
    quantity = models.TextField(null=True, blank=True)
    status = models.IntegerField(choices=ORDERSTATUS, default=1)
    pickup_time = models.TimeField(null=True, blank=True)
    payment_type = models.CharField(max_length =100, null=True, blank=True)
    price = models.CharField(max_length =100, null=True, blank=True)
    gst_amount = models.CharField(max_length =100, null=True, blank=True)
    total_amount = models.CharField(max_length =100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    productid = models.TextField(null=True, blank=True)
    quantity = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.user.user.username
    
class Review(models.Model):
    product = models.ForeignKey(Product_Master, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    ranking = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.user.username

class Staff(models.Model):
    username = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    userrole = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username
    
# class Country_Master(models.Model):
#     country_code=models.CharField(max_length=100, null=True, blank=True)    
#     country_name=models.CharField(max_length=100, null=True, blank=True)
#     country_currency=models.CharField(max_length=100, null=True)
#     country_flag=models.FileField(null=True, blank=True)

#     def __str__(self):
#         return self.country_name
    