from django.shortcuts import render
from django.shortcuts import render, redirect
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime
from . import models
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

# Create your views here.
@login_required
def index(request):
    return render(request,"base.html")

# ---------CATEGORY-------------

def category_list(request):
    categories = models.Category.objects.all()
    return render(request, 'category/list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        models.Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'category/create.html')

def category_update(request, code):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = models.Category.objects.get(code=code)
        category.name = name
        category.save()
        return redirect('category_list')
    category = models.Category.objects.get(code=code)
    return render(request, 'category/update.html', {'category': category})

def category_delete(request, code):
    category = models.Category.objects.get(code=code)
    category.delete()
    return redirect('category_list')

# ---------PRODUCT-------------

def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        category = models.Category.objects.get(id=category_id)
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        discount_price = request.POST.get('discount_price')
        banner_img = request.FILES.get('banner_img')
        print(request.POST)
        product = models.Product.objects.create(name=name, category=category, price=price, quantity=quantity, banner_img=banner_img)


        return redirect('product_list')
    else:
        categories = models.Category.objects.all()
        return render(request, 'product/create.html', {'categories': categories})

def product_list(request):
    products = models.Product.objects.all()
    return render(request, 'product/list.html', {'products': products})

def delete_product(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('product_list')

def update_product(request, code):
    product = models.Product.objects.get(code=code)
    categories = models.Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST['name']
        product.category_id = request.POST['category']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.discount_price = request.POST.get('discount_price', None)
        if 'banner_img' in request.FILES:
            product.banner_img = request.FILES['banner_img']
        product.save()
        return redirect('product_list')
    return render(request, 'product/update.html', {'product': product, 'categories':categories})
def product_detail(request, code):
    product = get_object_or_404(models.Product, code=code)
    return render(request, 'product/detail.html', {'product': product}) 

# ---------ENTER PRODUCT-------------

def create_enter_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = models.Product.objects.get(id=product_id)
        models.EnterProduct.objects.create(product=product, quantity=quantity)
        return redirect('enter_product_list')
    else:
        products = models.Product.objects.all()
        return render(request, 'enter_product/create.html', {'products': products})
    
def enter_product_detail(request, code):
    enter_product = get_object_or_404(models.EnterProduct, code=code)
    return render(request, 'enter_product/detail.html', {'enter_product': enter_product})
    
def enter_product_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    enter_products = models.EnterProduct.objects.all()

    if start_date and end_date:
        enter_products = enter_products.filter(entered_at__range=[start_date, end_date])

    return render(request, 'enter_product/list.html', {'enter_products': enter_products})

# ---------SELL PRODUCT-------------

def sellproduct_list(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    sell_products = models.SellProduct.objects.all()

    if start_date and end_date:
        sell_product = sell_products.filter(sold_at__range=[start_date, end_date])

    return render(request, 'sell_product/list.html', {'sell_products': sell_products})

def sellproduct_detail(request, code):
    sellproduct = get_object_or_404(models.SellProduct, code=code)
    return render(request, 'sell_product/detail.html', {'sellproduct': sellproduct})

def sellproduct_create(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        product = models.Product.objects.get(id=product_id)
        models.SellProduct.objects.create(product=product, quantity=quantity)
        return redirect('sellproduct_list')
    else:
        products = models.Product.objects.all()
        return render(request, 'sell_product/create.html', {'products': products})
    
def sellproduct_update(request, code):
    sellproduct = get_object_or_404(models.SellProduct, code=code)
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        refunded = request.POST.get('refunded', False)
        sellproduct.product_id = product_id
        sellproduct.quantity = quantity
        sellproduct.refunded = refunded
        sellproduct.save()
        return redirect('sellproduct_list')
    return render(request, 'sell_product/create.html', {'sellproduct': sellproduct})

# ---------REFUND-------------

def refund(request, code):
    sell_product = get_object_or_404(models.SellProduct, code=code)
    if not sell_product.refunded:
        if not models.Refund.objects.filter(sell_product=sell_product).exists():
            models.Refund.objects.create(sell_product=sell_product)
            sell_product.refunded = True
            sell_product.save()
            return redirect("sellproduct_list")
    return HttpResponse("The product has already been refunded.")

def refund_list(request):
    refunds = models.Refund.objects.all()
    return render(request, 'refund/list.html', {'refunds': refunds})

def refund_detail(request,id):
    refund = models.Refund.objects.get(id=id)
    return render(request,'refund/detail.html',{'refund':refund})

# ---------KIRIM CHIQIMLARNI HISOBLASH-------------
def filter(request):
    return render(request,'filter/filter.html')

def filter_entries(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        entries = models.EnterProduct.objects.filter(entered_at__gte=start_date, entered_at__lte=end_date)
        total_entries = entries.count()
        total_entries_price = entries.aggregate(Sum('price'))['price__sum'] or 0
        sales = models.SellProduct.objects.filter(sold_at__gte=start_date, sold_at__lte=end_date)
        total_sales = sales.count()
        total_sales_price = sales.aggregate(Sum('price'))['price__sum'] or 0
        total_price_per_product = sales.aggregate(Sum('product__price'))['product__price__sum'] or 0
        total_expenses = sales.aggregate(Sum('price'))['price__sum'] or 0 
        total_profit = total_entries_price - total_expenses
        if total_entries == 0 and total_sales == 0:
            return HttpResponseRedirect(reverse("filter"))

        context = {
            'entries': entries,
            'total_entries': total_entries,
            'total_entries_price': total_entries_price,
            'total_sales': total_sales,
            'total_sales_price': total_sales_price,
            'total_price_per_product': total_price_per_product,
            'total_expenses': total_expenses,
            'total_profit': total_profit,
        }
        
        return render(request,'filter/filter.html',context)

    return HttpResponseRedirect(reverse('filter')) 



# ---------AUTH-------------

def log_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return render(request,'auth/login.html')
        except:
            return redirect('index')
    return render(request, 'auth/login.html')


def log_out(request):
    logout(request)
    return redirect('index')

def edit_user(request):
    if request.method == 'POST':
        new_email = request.POST('email')
        new_username = request.POST('username')
        new_password = request.POST('password')
        superuser = User.objects.get(username=request.user.username)
        superuser.email = new_email
        superuser.username = new_username
        superuser.password = new_password
        superuser.save()
        return redirect('index')
    else:
        superuser = User.objects.get(username=request.user.username)
        return render(request, 'user/edit.html', {'superuser': superuser})