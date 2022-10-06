from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('signup/', signup_user, name='signup'),
    path('profile/', profile, name='profile'),
    path('edtprofile/',editprofile, name='editprofile'),
    path('signout/',signout, name='signout'),
    path('indexhome/',adminhome, name='adminhome'),
    path('registered-user/',registeredUser, name='registeredUser'),
    
    path('add-product-category/',addProductCategory, name='addProductCategory'),
    path('edit-product-category/<int:pid>/',addProductCategory, name='editProductCategory'),
    path('delete-product-category/<int:pid>/',deleteCategory, name='deleteCategory'),
    path('vwproduct-cateogy/',viewProductCategory, name='vwproductCategory'),
    
    path('add-product/',addProduct, name='addProduct'),
    path('edit-product/<int:pid>/',addProduct, name='editProduct'),
    path('delete-product/<int:pid>/',deleteProduct, name='deleteProduct'),
    path('vwproduct/',viewProduct, name='vwproduct'),
    
    path('change-status/<int:pid>/',changeStatus, name='change_status'),
    
    path('mycart/',mycart, name='mycart'),
    path('add_cart/<int:pid>/',add_cart, name='add_cart'),
    path('incredecre/<int:pid>/',incredecre, name='incredecre'),
    path('deletecart/<int:pid>/',deletecart, name='deletecart'),
    
    path('product/', product, name="product"),
    path('product-detail/<int:pid>/',product_detail, name="product-detail"),
    
    path('ordernow/<int:pid>/',ordernow, name="ordernow"),
    path('myorder/',myorder, name="myorder"),
    path('orderdetail/<int:pid>/',orderdetail, name="orderdetail"),
    path('invoice/<int:pid>/',invoice, name="invoice"),
    path('track-status/<int:pid>/',track_status, name="track_status"),
    path('delete-or-cancel-order/<int:pid>/',deleteOrCancelOrder, name="deleteOrCancelOrder"),
    
    path('contact/', contact, name="contact"),
    path('gallery/', gallery, name="gallery"),
    path('about/', about, name="about"),
    
    path('orderlist/', orderList, name="orderList"),
    path('admin-change-status/<int:pid>/', admin_change_status, name="admin_change_status"),
    path('change-tracking-status/<int:pid>/', change_tarcking_status, name="change_tarcking_status"),
    path('admin-order-detail/<int:pid>/', adminOrderDetail, name="adminOrderDetail"),
    
    path('change-password/', change_password, name="change_password"),

]
    