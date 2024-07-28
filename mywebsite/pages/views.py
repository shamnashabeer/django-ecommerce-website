from django.contrib.auth import  logout
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import View
from .models import Customer, Product, Cart 
from django.db.models import Count
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages

# Create your views here.
def home(request):
    template=loader.get_template("index.html")
    return HttpResponse(template.render())

def about(request):
    template=loader.get_template("about.html")
    return HttpResponse(template.render())

def contact(request):
    template=loader.get_template("contact.html")
    return HttpResponse(template.render())

class Categoryview(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request,"category.html",locals())
    
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,"category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)

        return render(request,"productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, "customerregistration.html",locals() )
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid  Input Data")
        return render(request, "customerregistration.html",locals() )

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'profile.html',locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'address.html',locals())


class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request,'updateaddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
def logoutUser(request):
    logout(request)
    return redirect('login')

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product= Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    # cart = Cart.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0
    for p in cart_items:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40  


    context = {
        'cart': cart_items,        
        'amount': amount,
        'totalamount': totalamount, }
    
    return render(request, 'app/addtocart.html', context)   

# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id=request.GET['prod_id']
#         print(prod_id)
#         data={

#         }
#         return JsonResponse(data)


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')  # Use get() to safely retrieve the value
        print(prod_id)  # Check if prod_id is correctly retrieved

        # Example data to return
        data = {
            'status': 'success',
            'prod_id': prod_id,
            # Add more data as needed
        }
        return JsonResponse(data)
