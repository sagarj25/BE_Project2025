import datetime
import json
import random
from webbrowser import get
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from CateringApp.forms import StaffForm
from CateringApp.send_email import sendemail
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
import matplotlib.pyplot as plt
import calendar
from django.db.models import Sum, Count
import os
import matplotlib.pyplot as plt
import pygal
from django.db.models.functions import TruncMonth
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from CateringApp.models import Product_Master, Order  # Import your models

# Create your views here.
def changeinInt(li):
    myli = []
    for i in li:
        myli.append(int(i))
    return myli


def breaklist(mystr):
    pid = mystr
    pid2 = pid[1:-1]
    
    if pid2 == "":
        return []
    else:
        pid3 = pid2.split(',')
        pid3 = changeinInt(pid3)
        return pid3


def myexistingid(li, pid, quantity):
    if pid in li:
        pindex = li.index(pid)
        qqty = int(quantity[pindex])
        qqty+=1
        quantity[pindex] = qqty
        return quantity, li
    else:
        quantity.append(1)
        li.append(pid)
        return quantity, li


def add_cart(request, pid):
    try:
        cart = Cart.objects.get(user__user=request.user)
        
        myli = breaklist(cart.productid)
        myliqty = breaklist(cart.quantity)
        myqty, myli = myexistingid(myli, pid, myliqty)
        
        cart.productid = myli
        cart.quantity = myqty
        cart.save()
    except:
        pidli = [pid]
        myuser = UserProfile.objects.get(user=request.user)
        cart = Cart.objects.create(user=myuser, productid=pidli, quantity=[1])
    return redirect('mycart')
        

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('adminhome')
    product = Product_Master.objects.filter(active=True)[:12]
    # oldprice=request.POST.get('price')

    return render(request, 'home.html', locals())


def contact(request):
    return render(request, 'contact.html', locals())


def gallery(request):
    product = Product_Master.objects.filter(active=True)
    # print("Products = ", product.count);
    return render(request, 'gallery.html', locals())


def about(request):
    return render(request, 'about.html', locals())


def login_user(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        user = authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('adminhome')
            elif user:
                data = UserProfile.objects.get(user=user)
                if data.status == 1:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('home')
                else:
                    messages.success(request, "Your are Inactive user, contact to administration.")
                    return redirect('login')
            else:
                messages.success(request, "Invalid Credentials")
                return redirect('login')
        except:
            messages.success(request, "Invalid Credentials")
            return redirect('login')
    return render(request, 'login.html')


def login_admin(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        user = authenticate(username=uname, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('adminhome')
            elif user:
                data = UserProfile.objects.get(user=user)
                if data.status == 1:
                    login(request, user)
                    messages.success(request, "Login Successful")
                    return redirect('home')
                else:
                    messages.success(request, "Your are Inactive user, contact to administration.")
                    return redirect('admin-login')
            else:
                messages.success(request, "Invalid Credentials")
                return redirect('admin-login')
        except:
            messages.success(request, "Invalid Credentials")
            return redirect('admin-login')
    return render(request, 'admin-login.html')


def send_otp(request):
    otp = ""
    for i in range(6):
        otp += str(random.randint(0, 9))
    mail = request.GET.get('mail')
    print("mail =", mail, request.GET, request.POST)
    try:
        userprofile = UserProfile.objects.get(user__username=mail)
        userprofile.otp = otp
        userprofile.save()
        subject = "OTP Generation"
        html_content = "<h4><b>Your One-Time-Password for changing password is '"+otp+"'. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
        check_mail = None
        try:
            check_mail = sendemail(userprofile.user.email, subject, html_content)
            if check_mail:
                return JsonResponse({'status':True})
            else:
                return JsonResponse({'status':False})
        except:
            return JsonResponse({'status':False})
    except:
        return JsonResponse({'status':False})


def match_otp(request):
    otp = request.GET.get('otp')
    mail = request.GET.get('mail')
    try:
        userprofile = UserProfile.objects.get(user__username=mail)
        if userprofile.otp == otp:
            return JsonResponse({'status':True})
        else:
            return JsonResponse({'status':False})
    except:
        return JsonResponse({'status':False})


def forgot_password(request):
    return render(request, 'forgot-password.html', locals())


def signup_user(request):
    if request.method == 'POST':
        # uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        image = request.FILES.get('file')
        subject = "Registeration Successful"
        html_content = "<h4><b>Thanks, For registered with us. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
        check_mail = None
        try:
            user = User.objects.create_user(username=email, email=email, first_name=fname, last_name=lname, password=pwd)
            check_mail = sendemail(email, subject, html_content)
        except:
            pass
        if check_mail:
            userprofile = UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
            messages.success(request, "Registration completed")
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False})
    return render(request, 'registration.html')


def profile(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    data = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', locals())


def editprofile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mobile = request.POST.get('mobile')
        try:
            image = request.FILES['file']
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.image=image
            userprofile.save()
        except:
            pass
        user = User.objects.filter(username=uname).update(first_name=fname, last_name=lname)
        userprofile = UserProfile.objects.filter(user=user).update(mobile=mobile)
        messages.success(request, "Profile Updated")
        return redirect('profile')
    data=UserProfile.objects.get(user=request.user)
    return render(request, 'editprofile.html', locals())


def signout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('home')
   
 
def adminhome(request):
    tcust = UserProfile.objects.filter()
    tprod = Product_Master.objects.filter()
    tdbook = Order.objects.filter(created__date=datetime.date.today())
    tbook = Order.objects.filter()
    tprodcat = Product_Category.objects.filter()
    trev = Review.objects.filter()
    tdel = Order.objects.filter(status=5)
    tact = UserProfile.objects.filter(status=1)
    graph_image_path = monthly_sales_bar_graph(request)
    graph_image_pie_path = monthly_sales_pie_chart(request)
    return render(request, 'adminhome.html', locals())


def registeredUser(request):
    status = request.GET.get('status')
    data = UserProfile.objects.all()
    if status:
        data = UserProfile.objects.filter(status=status)
    return render(request, 'registeredUser.html', locals())


def changeStatus(request, pid):
    data = UserProfile.objects.get(id=pid)
    if data.status == 1:
        data.status = 2
    else:
        data.status = 1
    data.save()
    messages.success(request, "Status Changed")
    return redirect('registeredUser')


def addProductCategory(request, pid=None):
    data = None
    if pid:
        data = Product_Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST.get('category')
        image = ""
        try:
            image = request.FILES['image']
        except:
            pass
        if pid:
            prod_cat = Product_Category.objects.filter(id=pid).update(name=name, createdby=request.user.id)
            if image:
                data.image = image
                data.save()
            messages.success(request, "Category Updated")
        else:
            Product_Category.objects.create(name=name, createdby=request.user.id, image=image)
            messages.success(request, "Category Added")
        
        return redirect('vwproductCategory')
    return render(request, "add_product_category.html", locals())


def viewProductCategory(request):
    action = request.GET.get('action')
    category = Product_Category.objects.filter()
    if action == "inactive":
       category = category.filter(active=False)
    elif action == "active":
        category = category.filter(active=True)
    return render(request, 'viewCategory.html', locals())


def deleteCategory(request, pid):
    data = Product_Category.objects.get(id=pid)
    # data.delete()
    if data.active:
        data.active = False
        messages.success(request, "Category Deleted")
    else:
        data.active = True
        messages.success(request, "Category Recalled")
    data.save()
    
    return redirect('vwproductCategory')


def addProduct(request, pid=None):
    data = None
    if pid:
        data = Product_Master.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST.get('products')
        price = request.POST.get('price')
        desc =request.POST.get('desc')
        detaildesc =request.POST.get('editor1')
        cat =request.POST.get('category')
        datacat = Product_Category.objects.get(id=cat)
        if pid:
            try:
                image=request.FILES['image']
                data.image = image
                data.save()
            except:
                pass
            Product_Master.objects.filter(id=pid).update(category=datacat,name=name,price=price,desc=desc,createdby=request.user.id, detaildesc=detaildesc)
            messages.success(request, "Product Updated")
        else:
            image=request.FILES.get('image')
            Product_Master.objects.create(category=datacat,name=name,price=price,desc=desc,image=image,createdby=request.user.id, detaildesc=detaildesc)
            messages.success(request, "Product Added")
        return redirect('vwproduct')
    category = Product_Category.objects.filter(active=True)
    return render(request, "add_product.html", locals())


def deleteProduct(request, pid):
    data = Product_Master.objects.get(id=pid)
    # data.delete()
    if data.active:
        data.active = False
        messages.success(request, "Product Deleted")
    else:
        data.active = True
        messages.success(request, "Product Recalled")
    data.save()
    
    return redirect('vwproduct')


def viewProduct(request):
    action = request.GET.get('action')
    proid = request.GET.get('proid')
    product = Product_Master.objects.filter()
    if request.method == "POST":
        file = request.FILES.getlist('file-'+proid+'[]')
        pro = Product_Master.objects.get(id=proid)
        for i in file:
            ProductImage.objects.create(product=pro, image=i)
            print(i.name)
            
    if action == "inactive":
        product = product.filter(active=False)
    elif action == "active":
        product = product.filter(active=True)
    return render(request, 'viewProduct.html', locals())


def mycart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    getcountry = request.GET.get('country')
    state = None
    productid = []
    try:
        cart = Cart.objects.get(user__user=request.user)
        myli = breaklist(cart.productid)
        productid = myli
    except:
        productid = []
    f = open(str(settings.BASE_DIR)+'/CateringApp/static/json/gistfile1.json')
    data = json.load(f)
    country = data['countries']
    if getcountry:
        for i in country:
            if i['country'] == getcountry: 
                state = i['states']
                break
    lengthpro = len(productid)
    return render(request, 'mycart.html', locals())


def incredecre(request, pid):
    cart = Cart.objects.get(user__user=request.user)
    qtyli = breaklist(cart.quantity)
    proli = breaklist(cart.productid)
    pindex = proli.index(pid)
    qqty = int(qtyli[pindex])

    action = request.GET.get('action')
    if action == "1":
        qqty += 1
    elif action == "2":
        qqty -= 1
    qtyli[pindex] = qqty
    cart.quantity = qtyli
    cart.save()
    return redirect('mycart')


def deletecart(request, pid):
    cart = Cart.objects.get(user__user=request.user)
    qtyli = breaklist(cart.quantity)
    proli = breaklist(cart.productid)
    pindex = proli.index(pid)

    qtyli.pop(pindex)
    proli.pop(pindex)
    cart.quantity = qtyli
    cart.productid = proli
    cart.save()
    messages.success(request, "Remove a item from cart.")
    return redirect('mycart')


def product(request):
    search  = request.GET.get('search')
    cat_param = request.GET.get('category', None)
    product = Product_Master.objects.filter(active=True)
    if search:
        product = product.filter(name__icontains=search)
    latestproduct = Product_Master.objects.filter(active=True).order_by('-id')[:2]
    if cat_param:
        product = product.filter(category__id=cat_param)
    paginator = Paginator(product, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category = Product_Category.objects.filter(active=True)
    return render(request, 'product.html', locals())


def product_detail(request, pid):
    data = Product_Master.objects.get(id=pid)
    if request.method == 'POST':
        if request.user.is_authenticated:
            return redirect('login')
        starval = request.POST.get('starval')
        comment = request.POST.get('comment')
        userprofile = UserProfile.objects.get(user=request.user)
        Review.objects.create(comment=comment, ranking=starval, user=userprofile, product=data)
        messages.success(request, "Your Review has been created")
        return redirect('product-detail', pid)
    product = Product_Master.objects.filter(active=True)
    return render(request, 'product_detail.html', locals())

    
def ordernow(request, pid):
    cart = Cart.objects.get(id=pid)
    total = request.GET.get('total')
    original_total = request.GET.get('original_total')
    tax = request.GET.get('tax')
    print(request.GET)
    pickup_time = request.GET.get('pickup_time')
    payment_type = request.GET.get('payment_type')
    subject = "Payment Successful."
    html_content = "<h4><b>Thanks, Your order has been placed successfully, After preparing food we will notify soon!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
    check_mail = sendemail(request.user.email, subject, html_content)
    Order.objects.create(user=cart.user, productid=cart.productid, payment_type=payment_type, pickup_time=pickup_time, quantity=cart.quantity, price=original_total, gst_amount=tax, total_amount=total)
    messages.success(request, "Ordered Sucessfully")
    cart.productid = []
    cart.quantity = []
    cart.save()
    return redirect('myorder')


def payment(request, pid):
    cart = Cart.objects.get(id=pid)
    payment_type = request.GET.get('payment_type')
    total = request.GET.get('total')
    original_total = request.GET.get('original-total')
    tax = request.GET.get('tax')
    pickup_time = request.GET.get('pickup_time')
    if payment_type != 'Online Payment':
        return redirect('/ordernow/'+str(pid)+'/?total='+total+'&pickup_time='+pickup_time+'&payment_type='+payment_type+'&original_total='+original_total+'&tax='+tax)


    if request.method == "POST":
        print(request.POST)
        payment_type = request.POST.get('payment_type')
        total = request.POST.get('total')
        original_total = request.POST.get('original_total')
        tax = (request.POST.get('tax'))
        pickup_time = request.POST.get('pickup_time')
        print(payment_type, total, pickup_time)
        return redirect('/ordernow/'+str(pid)+'/?total='+total+'&pickup_time='+pickup_time+'&payment_type='+payment_type+'&original_total='+original_total+'&tax='+tax)
    return render(request, 'payment.html', locals())


def change_date_month(obj_date, new_month):
    # Create a new date object with the desired month
    new_date = datetime.date(obj_date.year, new_month, obj_date.day)
    
    return new_date


def myorder(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # your_object = Order.objects.get(id=2)
    # new_date = change_date_month(your_object.created, 5)  # Change to July (month number 7)
    # new_date2 = change_date_month(your_object.updated, 5)  # Change to July (month number 7)
    # your_object.created = new_date
    # your_object.updated = new_date2
    # your_object.save()
    order = Order.objects.filter(user__user=request.user, active=True)
    return render(request, 'myorder.html', locals())


def orderdetail(request, pid):
    order = Order.objects.get(id=pid)
    myli = breaklist(order.productid)
    productid = myli
    lengthpro = len(productid)
    
    return render(request, 'orderdetail.html', locals())


def add_comment(request, pid, oid):
    data = Product_Master.objects.get(id=pid)
    if request.method == 'POST':
        starval = request.POST.get('starval')
        comment = request.POST.get('comment')
        userprofile = UserProfile.objects.get(user=request.user)
        Review.objects.create(comment=comment, ranking=starval, user=userprofile, product=data)
        messages.success(request, "Your Review has been created")
    return redirect('orderdetail', oid)


def invoice(request, pid):
    order = Order.objects.get(id=pid)
    myli = breaklist(order.productid)
    productid = myli
    lengthpro = len(productid)
    return render(request, 'invoice.html', locals())


def deleteOrCancelOrder(request, pid):
    order = Order.objects.get(id=pid)
    action = request.GET.get('action')
    
    if action == "cancel":
        if order.status < 3:
            order.status = 6
            subject = "Order Cancel"
            html_content = "<h4><b>Your order has been cancelled, we are processing refund you will get it in 7 working days. If any query you can you query, So i can give you a better service next time.Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
            check_mail = sendemail(order.user.user.email, subject, html_content)
            messages.success(request, "Order Canceled")

    elif action == "delete":
        if order.active:
            order.active = False
        else:
            order.active = True
        messages.success(request, "Order Deleted")
            
    else:
        pass
    
    order.save()
    
    if request.user.is_staff:
        if request.GET.get('active'):
            return HttpResponseRedirect("/orderlist/?status="+request.GET.get('status')+"&order="+request.GET.get('order')+"&active=1")
        return HttpResponseRedirect("/orderlist/?status="+request.GET.get('status')+"&order="+request.GET.get('order'))
    
    return redirect('myorder')


def all_review(request):
    review = Review.objects.filter(active=True)
    return render(request, 'all-reviews.html', locals())


def delete_review(request, pid):
    review = Review.objects.get(id=pid)
    review.delete()
    messages.success(request, "Review Deleted Successfully.")
    return redirect('all-review')


def orderList(request):
    order = Order.objects.filter(active=True)
    status = None
    action_for = None
    try:
        status = int(request.GET.get('status'))
    except:
        action_for = request.GET.get('status')
    action = request.GET.get('active')
    if status:
        order = order.filter(status=status)
    if action == '1':
        order = order.filter(active=False)
    if action_for == 'today':
        order = Order.objects.filter(created__date=datetime.date.today())
    return render(request, 'orderlist.html', locals())


def admin_change_status(request, pid):
    order = Order.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    if request.method == 'POST':
        status = int(request.GET.get('status'))
        if status == 4:
            subject = "Order Ready"
            html_content = "<h4><b>Now, Your order is ready for pickup!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
            check_mail = sendemail(order.user.user.email, subject, html_content)
        if status == 5:
            subject = "Order Complete"
            html_content = "<h4><b>Your order has been completed. Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
            check_mail = sendemail(order.user.user.email, subject, html_content)
        if status == 6:
            subject = "Order Cancel"
            html_content = "<h4><b>Your order has been cancelled, we are processing refund you will get it in 7 working days. If any query you can you query, So i can give you a better service next time.Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
            check_mail = sendemail(order.user.user.email, subject, html_content)
        if status == 7:
            subject = "Refund Complete"
            html_content = "<h4><b>Your refund has been completed now. If any query you can you query, So i can give you a better service next time.Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
            check_mail = sendemail(order.user.user.email, subject, html_content)
        order.status = status
        order.save()
        return redirect('orderList')
    return render(request, 'admin_change_status.html', locals())


def track_status(request, pid):
    order = Order.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, 'track_status.html', locals())


def change_tarcking_status(request, pid):
    order = Order.objects.get(id=pid)
    status = request.GET.get('status')
    status = int(request.GET.get('status'))
    if status == 4:
        subject = "Order Ready"
        html_content = "<h4><b>Now, Your order is ready for pickup!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
        check_mail = sendemail(order.user.user.email, subject, html_content)
    if status == 5:
        subject = "Order Complete"
        html_content = "<h4><b>Your order has been completed. Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
        check_mail = sendemail(order.user.user.email, subject, html_content)
    if status == 6:
        subject = "Order Cancel"
        html_content = "<h4><b>Your order has been cancelled, we are processing refund you will get it in 7 working days. If any query you can you query, So i can give you a better service next time.Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
        check_mail = sendemail(order.user.user.email, subject, html_content)
    if status == 7:
        subject = "Refund Complete"
        html_content = "<h4><b>Your refund has been completed now. If any query you can you query, So i can give you a better service next time.Thank you!. </b></h4><br><br><h5>Thanks & Regards<br>Canteen Management</h5>"
        check_mail = sendemail(order.user.user.email, subject, html_content)
    order.status = status
    order.save()
    messages.success(request, "Status Changed")
    return JsonResponse({'msg':"Status Changed"})


def adminOrderDetail(request, pid):
    order = Order.objects.get(id=pid)
    myli = breaklist(order.productid)
    productid = myli
    lengthpro = len(productid)
    return render(request, 'admin_order_detail.html', locals())


def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        action = request.GET.get('action')
        user = None
        if action == 'forgot-password':
            email = request.GET.get('email')
            user = User.objects.get(username=email)
        else:
            user = authenticate(username=request.user.username, password=o)
        if user: 
            if n == c:
                user.set_password(n)
                user.save()
                messages.success(request, "Password Changed")
                return redirect('home')
            else:
                messages.success(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.success(request, "Invalid Password")
            return redirect('change_password')
    if request.user.is_staff:
        return render(request, 'admin_password.html')
    return render(request, 'change_password.html')


def report_generation(request):
    from_date = None
    to_date = None
    orderlist = None
    if request.method == "POST":
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        orderlist = Order.objects.filter(created__gte=from_date, created__lte=to_date)
    return render(request,'reportgeneration.html', locals())


def add_staff(request, pid=None):
    staff = None
    if pid:
        staff = Staff.objects.get(id=pid)
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            new_staff = form.save()
            messages.success(request, "Staff saved successfully.")
            return redirect('view-staff')
    return render(request, 'add_staff.html', locals())


def view_staff(request):
    data = Staff.objects.all()
    return render(request, 'view-staff.html', locals())


def delete_staff(request, pid):
    staff = Staff.objects.get(id=pid)
    staff.delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('view-staff')


@csrf_exempt
def monthly_sales_bar_graph(request):
    # Get the monthly sales for all products
    monthly_sales = Order.objects.filter(active=True) \
                                .values('created__year', 'created__month') \
                                .annotate(total_sales=Sum('price'))

    # Extract the year and month values from the queryset
    years = [sale['created__year'] for sale in monthly_sales]
    months = [sale['created__month'] for sale in monthly_sales]

    # Get the month names based on the month values
    month_names = [calendar.month_name[month] for month in months]

    # Get the total sales for each month
    sales_data = [sale['total_sales'] for sale in monthly_sales]

    # Prepare the chart data
    chart_data = {
        'labels': month_names,
        'datasets': [
            {
                'label': 'Total Sales',
                'data': sales_data,
                'backgroundColor': 'rgba(54, 162, 235, 0.5)'
            }
        ]
    }

    # Return the chart data as a JSON response
    return JsonResponse(chart_data)


@csrf_exempt
def monthly_sales_pie_chart(request):
    # Get the monthly sales
    monthly_sales = Order.objects.filter(active=True) \
                                .annotate(month=TruncMonth('created')) \
                                .values('month') \
                                .annotate(total_sales=Sum('price'))

    # Extract the month labels and total sales
    months = [sale['month'].strftime('%B %Y') for sale in monthly_sales]
    total_sales = [sale['total_sales'] for sale in monthly_sales]

    # Prepare the chart data
    chart_data = {
        'labels': months,
        'datasets': [
            {
                'data': total_sales,
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                ]
            }
        ]
    }

    # Return the chart data as a JSON response
    return JsonResponse(chart_data)


def delete_existing_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)




