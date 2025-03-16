from django.urls import path
from .views import *

from django.urls import path, include
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_user, name='login'),
    path('admin-login/', login_admin, name='admin-login'),
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
    
    path('all-review/', all_review, name="all-review"),
    path('delete-or-cancel-review/<int:pid>/', delete_review, name="delete-or-cancel-review"),
    path('orderlist/', orderList, name="orderList"),
    path('admin-change-status/<int:pid>/', admin_change_status, name="admin_change_status"),
    path('change-tracking-status/<int:pid>/', change_tarcking_status, name="change_tarcking_status"),
    path('admin-order-detail/<int:pid>/', adminOrderDetail, name="adminOrderDetail"),
    path('admin-report-generation/', report_generation, name="adminreportgeneration"),
    
    path('change-password/', change_password, name="change_password"),
    path('add-staff/', add_staff, name="add_staff"),
    path('change-staff/<int:pid>/', add_staff, name="change-staff"),
    path('delete-staff/<int:pid>/', delete_staff, name="delete-staff"),
    path('add-comment/<int:pid>/<int:oid>/', add_comment, name="add-comment"),
    path('view-staff/', view_staff, name="view-staff"),
    path('monthly_sales_bar_graph/', monthly_sales_bar_graph, name='monthly_sales_bar_graph'),
    path('monthly_sales_pie_chart/', monthly_sales_pie_chart, name='monthly_sales_pie_chart'),

    path('payment/<int:pid>/', payment, name="payment"),
    path('forgot-password/', forgot_password, name="forgot-password"),
    path('send-otp/', send_otp, name="send-otp"),
    path('match-otp/', match_otp, name="match-otp"),

    
    
]
    