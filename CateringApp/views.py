import datetime
import json
from webbrowser import get
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator


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

def signup_user(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        image = request.FILES['file']
        user = User.objects.create_user(username=uname, email=email, first_name=fname, last_name=lname, password=pwd)
        userprofile = UserProfile.objects.create(user=user, mobile=mobile, address=address, image=image)
        messages.success(request, "Registration completed")
        return redirect('login')
    return render(request, 'registration.html')

@login_required(login_url='/login/') #redirect when user is not logged in
def profile(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    data = UserProfile.objects.get(user=request.user)
    return render(request, 'profile.html', locals())

@login_required(login_url='/login/')
def editprofile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        uname = request.POST.get('uname')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        try:
            image = request.FILES['file']
            userprofile = UserProfile.objects.get(user=request.user)
            userprofile.image=image
            userprofile.save()
        except:
            pass
        user = User.objects.filter(username=uname).update(email=email, first_name=fname, last_name=lname)
        userprofile = UserProfile.objects.filter(user=user).update(mobile=mobile, address=address)
        messages.success(request, "Profile Updated")
        return redirect('profile')
    data=UserProfile.objects.get(user=request.user)
    return render(request, 'editprofile.html', locals())

def signout(request):
    logout(request)
    messages.success(request, "Logout successfully")
    return redirect('home')
   
@login_required(login_url='/login/') 
def adminhome(request):
    tcust = UserProfile.objects.filter()
    tprod = Product_Master.objects.filter()
    tdbook = Order.objects.filter(created__date=datetime.date.today())
    tbook = Order.objects.filter()
    tprodcat = Product_Category.objects.filter()
    trev = Review.objects.filter()
    tdel = Order.objects.filter(status=5)
    tact = UserProfile.objects.filter(status=1)
    return render(request, 'adminhome.html', locals())

@login_required(login_url='/login/')
def registeredUser(request):
    status = request.GET.get('status')
    data = UserProfile.objects.all()
    if status:
        data = UserProfile.objects.filter(status=status)
    return render(request, 'registeredUser.html', locals())

@login_required(login_url='/login/')
def changeStatus(request, pid):
    data = UserProfile.objects.get(id=pid)
    if data.status == 1:
        data.status = 2
    else:
        data.status = 1
    data.save()
    messages.success(request, "Status Changed")
    return redirect('registeredUser')

@login_required(login_url='/login/')
def addProductCategory(request, pid=None):
    data = None
    if pid:
        data = Product_Category.objects.get(id=pid)
    if request.method == 'POST':
        name = request.POST.get('category')
        if pid:
            Product_Category.objects.filter(id=pid).update(name=name, createdby=request.user.id)
            messages.success(request, "Category Updated")
        else:
            Product_Category.objects.create(name=name, createdby=request.user.id)
            messages.success(request, "Category Added")
        
        return redirect('vwproductCategory')
    return render(request, "add_product_category.html", locals())


@login_required(login_url='/login/')
def viewProductCategory(request):
    action = request.GET.get('action')
    category = Product_Category.objects.filter()
    if action == "inactive":
       category = category.filter(active=False)
    elif action == "active":
        category = category.filter(active=True)
    return render(request, 'viewCategory.html', locals())


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def mycart(request):
    getcountry = request.GET.get('country')
    state = None
        
    productid = []
    try:
        cart = Cart.objects.get(user__user=request.user)
        myli = breaklist(cart.productid)
        productid = myli
        # print("My List = ", type(productid), productid)
    except:
        productid = []
    f = open(str(settings.BASE_DIR)+'/CateringApp/static/json/gistfile1.json')
    data = json.load(f)
    country = data['countries']
    print(type(country))
    if getcountry:
        for i in country:
            if i['country'] == getcountry: 
                state = i['states']
                break
    
    lengthpro = len(productid)
    return render(request, 'mycart.html', locals())


@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
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
    product = Product_Master.objects.filter(active=True)
    if search:
        product = product.filter(name__icontains=search)
    
    latestproduct = Product_Master.objects.filter(active=True).order_by('-id')[:4]
    paginator = Paginator(product, 6) # Show 25 contacts per page.

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

    
@login_required(login_url='/login/')
def ordernow(request, pid):
    cart = Cart.objects.get(id=pid)
    if request.method == 'POST':
        country = request.POST.get('country')
        state = request.POST.get('state')
        zip = request.POST.get('zipcode')
        total = request.POST.get('total')
        Order.objects.create(user=cart.user, productid=cart.productid, country=country, state=state, quantity=cart.quantity, price=total, zipcode=zip)
        messages.success(request, "Ordered Sucessfully")
        
        cart.productid = []
        cart.quantity = []
        cart.save()
    return redirect('home')

@login_required(login_url='/login/')
def myorder(request):
    order = Order.objects.filter(user__user=request.user, active=True)
    return render(request, 'myorder.html', locals())

@login_required(login_url='/login/')
def orderdetail(request, pid):
    order = Order.objects.get(id=pid)
    myli = breaklist(order.productid)
    productid = myli
    lengthpro = len(productid)
    return render(request, 'orderdetail.html', locals())


@login_required(login_url='/login/')
def invoice(request, pid):
    order = Order.objects.get(id=pid)
    myli = breaklist(order.productid)
    productid = myli
    lengthpro = len(productid)
    return render(request, 'invoice.html', locals())


@login_required(login_url='/login/')
def deleteOrCancelOrder(request, pid):
    order = Order.objects.get(id=pid)
    action = request.GET.get('action')
    match action:
        case "cancel":
            if order.status < 5:
                order.status = 6
                messages.success(request, "Order Canceled")

        case "delete":
            if order.active:
                order.active = False
            else:
                order.active = True
            messages.success(request, "Order Deleted")

        case "return":
            order.status = 7
            messages.success(request, "Return Initiated")
            
        case _:
            pass
    order.save()
    if request.user.is_staff:
        if request.GET.get('active'):
            return HttpResponseRedirect("/orderlist/?status="+request.GET.get('status')+"&order="+request.GET.get('order')+"&active=1")
        return HttpResponseRedirect("/orderlist/?status="+request.GET.get('status')+"&order="+request.GET.get('order'))
    return redirect('myorder')


def orderList(request):
    order = Order.objects.filter(active=True)
    status = request.GET.get('status')
    action = request.GET.get('active')
    if status:
        order = order.filter(status=status)
    if action == '1':
        order = Order.objects.filter(active=False)
        if status:
            order = order.filter(status=status)
    return render(request, 'orderlist.html', locals())

def admin_change_status(request, pid):
    order = Order.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    if request.method == 'POST':
        status = request.POST.get('status')
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
    if status:
        order.status = status
    order.save()
    messages.success(request, "Status Changed")
    return JsonResponse({'msg':"Status Changed"})

@login_required(login_url='/login/')
def adminOrderDetail(request, pid):
    order = Order.objects.get(id=pid)
    myli = breaklist(order.productid)
    productid = myli
    lengthpro = len(productid)
    return render(request, 'admin_order_detail.html', locals())

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
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
        