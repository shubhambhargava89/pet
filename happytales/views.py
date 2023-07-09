from datetime import date
from django import views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm, feedbackForm, reportForm
from django.contrib import messages
from happytales import models
from happytales.models import Customer
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from .serializers import CustomerSerializer, OrderPlacedSerializer, ProductSerializer, CartSerializer, \
    FeedbackSerializer
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


@csrf_exempt
def customer(request):
    if request.method == "GET":
        regis = Customer.objects.all()
        print("students = ", regis)
        serializer = CustomerSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")


@csrf_exempt
def product(request):
    if request.method == "GET":
        regis = Product.objects.all()
        print("students = ", regis)
        serializer = ProductSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")


@csrf_exempt
def carts(request):
    if request.method == "GET":
        regis = Cart.objects.all()
        print("students = ", regis)
        serializer = CartSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")


@csrf_exempt
def orderplaced(request):
    if request.method == "GET":
        regis = OrderPlaced.objects.all()
        print("students = ", regis)
        serializer = OrderPlacedSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")


@csrf_exempt
def feedback(request):
    if request.method == "GET":
        regis = Feedback.objects.all()
        print("students = ", regis)
        serializer = FeedbackSerializer(regis, many=True)
        print("serializer = ", serializer.data)
        return JsonResponse(serializer.data, safe=False, status=200)
    return HttpResponse("success")


class ProductView(View):
    def get(self, request):
        totalitem = 0
        dog = Product.objects.filter(category='do')
        cat = Product.objects.filter(category='ca')
        catfood = Product.objects.filter(category='cf')
        dogfood = Product.objects.filter(category='df')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'home.html',
                      {'dog': dog, 'dogfood': dogfood, 'cat': cat, 'catfood': catfood,
                       'totalitem': totalitem, })


class ProductDetailView(View):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'productdetail.html',
                      {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})


@login_required
def add_to_cart(request):
    totalitem = 0
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('/cart', {'totalitem': totalitem})


def show_cart(request):
    if request.user.is_authenticated:
        totalitem = 0
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount,
                                                      'shipping_amount': shipping_amount, 'totalitem': totalitem})
        else:
            return render(request, 'emptycart.html')


def buy_now(request):
    return render(request, 'buynow.html')


def address(request):
    totalitem = 0
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'address.html', {'add': add, 'active': 'btn-warning', 'totalitem': totalitem})


def orders(request):
    totalitem = 0
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'orders.html', {'order_placed': op, 'totalitem': totalitem})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations!! You are registered Successfully.')
        return render(request, 'customerregistration.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class Feedbacks(View):
    def get(self, request):
        form = feedbackForm()
        return render(request, 'feedback.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = feedbackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            description = form.cleaned_data['description']
            reg = Feedback(name=name, mobile=mobile, city=city, pincode=pincode, state=state, description=description)
            reg.save()
            messages.success(request, 'Congratulations!! Feedback Submit Successfully.')
        return render(request, 'feedback.html', {'form': form, 'active': 'btn-primary'})


@login_required
def checkout(request):
    totalitem = 0
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
    totalamount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'checkout.html',
                  {'add': add, 'totalamount': totalamount, 'cart_items': cart_items, 'totalitem': totalitem})


def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()

    return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    totalitem = 0

    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html', {'form': form, 'active': 'btn-warning', 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, mobile=mobile, locality=locality, city=city, state=state,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html', {'form': form, 'active': 'btn-warning', 'totalitem': totalitem})


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1 < 5
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }

        return JsonResponse(data)


def cat(request, data=None):
    totalitem = 0
    if data == None:
        cat = Product.objects.filter(category='ca')
    elif data == 'below':
        cat = Product.objects.filter(category='ca').filter(discounted_price__lt=500)
    elif data == 'above':
        cat = Product.objects.filter(category='ca').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        cat = len(Cart.objects.filter(user=request.user))
    return render(request, 'cat.html', {'cat': cat, 'totalitem': totalitem})


def catfood(request, data=None):
    totalitem = 0
    if data == None:
        catfood = Product.objects.filter(category='cf')
    elif data == 'below':
        catfood = Product.objects.filter(category='cf').filter(discounted_price__lt=500)
    elif data == 'above':
        catfood = Product.objects.filter(category='cf').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'catfood.html', {'catfood': catfood, 'totalitem': totalitem})


def dog(request, data=None):
    totalitem = 0
    if data == None:
        dog = Product.objects.filter(category='do')
    elif data == 'below':
        dog = Product.objects.filter(category='do').filter(discounted_price__lt=500)
    elif data == 'above':
        dog = Product.objects.filter(category='do').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'dog.html', {'dog': dog, 'totalitem': totalitem})


def dogfood(request, data=None):
    totalitem = 0
    if data == None:
        dogfood = Product.objects.filter(category='df')
    elif data == 'below':
        dogfood = Product.objects.filter(category='df').filter(discounted_price__lt=500)
    elif data == 'above':
        dogfood = Product.objects.filter(category='df').filter(discounted_price__gt=500)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'dogfood.html', {'dogfood': dogfood, 'totalitem': totalitem})


class Report(View):
    def get(self, request):
        form = reportForm()
        return render(request, 'report.html', {'form': form, 'active': 'btn-primary'})

    def post(self, request):
        form = reportForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            state = form.cleaned_data['state']
            pet_type = form.cleaned_data['pet_type']
            pet_breed = form.cleaned_data['pet_breed']
            pet_location = form.cleaned_data['pet_location']
            description = form.cleaned_data['description']
            reg = Report(name=name, mobile=mobile, city=city, pincode=pincode, state=state, pet_type=pet_type,
                         pet_breed=pet_breed,
                         pet_location=pet_location, description=description)
            reg.save()
            messages.success(request, 'Congratulations!! Report Submit Successfully.')
        return render(request, 'report.html', {'form': form, 'active': 'btn-primary'})


# def SignUp(request):
#     if request.method == 'POST':F
#         form = UserCreateForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             first_name = user.first_name
#             last_name = user.last_name
#             name = first_name + ' ' + last_name
#             return render(request, 'signup.html', {'form': form})
#     else:
#         form = UserCreateForm()
#     return render(request, 'signup.html', {'form': form})

def donor_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Donor.objects.get(user=user)
                if user1.type == "Donor":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'donor_login.html', d)


def donor_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Donor.objects.create(user=user, mobile=con, image=i, gender=gen, type="Donor")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'donor_signup.html', d)


def donor_home(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    user = request.user
    donor = Donor.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        donor.user.first_name = f
        donor.user.last_name = l
        donor.mobile = con
        donor.gender = gen

        try:
            donor.save()
            donor.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            donor.image = i
            donor.save()
            error = "no"
        except:
            pass
    d = {'donor': donor, 'error': error}

    return render(request, 'donor_home.html', d)


def pet_list(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    user = request.user
    donor = Donor.objects.get(user=user)
    pet = Pet.objects.filter(donor=donor)
    d = {'pet': pet}
    return render(request, 'pet_list.html', d)


def delete_pet(request, pid):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    pet = Pet.objects.get(id=pid)
    pet.delete()
    return redirect('pet_list')


def edit_pet(request, pid):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    error = ""
    pet = Pet.objects.get(id=pid)
    if request.method == "POST":
        pn = request.POST['name']
        pt = request.POST['pettype']
        va = request.POST['vaccination']
        sd = request.POST['postdate']
        ed = request.POST['breed']
        sal = request.POST['price']
        loc = request.POST['location']
        ag = request.POST['age']
        col = request.POST['color']
        wei = request.POST['weight']
        des = request.POST['description']

        pet.pet_name = pn
        pet.pet_type = pt
        pet.vaccinated = va
        pet.pet_breed = ed
        pet.price = sal
        pet.location = loc
        pet.age = ag
        pet.color = col
        pet.weight = wei
        pet.description = des
        try:
            pet.save()
            error = "no"
        except:
            error = "yes"
        if sd:
            try:
                pet.post_date = sd
                pet.save()
            except:
                pass
        else:
            pass
        try:
            i = request.FILES['image']
            pet.image = i
            pet.save()
            error = "no"
        except:
            pass

    d = {'error': error, 'pet': pet}
    return render(request, 'edit_pet.html', d)


def add_pet(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    error = ""
    if request.method == "POST":
        pn = request.POST['name']
        pt = request.POST['pettype']
        va = request.POST['vaccination']
        sd = request.POST['postdate']
        ed = request.POST['breed']
        sal = request.POST['price']
        loc = request.POST['location']
        ag = request.POST['age']
        col = request.POST['color']
        wei = request.POST['weight']
        l = request.FILES['image']
        des = request.POST['description']
        user = request.user
        donor = Donor.objects.get(user=user)
        try:
            Pet.objects.create(donor=donor, post_date=sd, pet_name=pn, pet_type=pt, vaccinated=va, pet_breed=ed,
                               price=sal, location=loc, age=ag, color=col, weight=wei, image=l,
                               description=des, creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_pet.html', d)


def adopter_list(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    data = Buy.objects.all()
    d = {'data': data}
    return render(request, 'adopter_list.html', d)


def donor_changepassword(request):
    if not request.user.is_authenticated:
        return redirect('donor_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'donor_changepassword.html', d)


def adopter_changepassword(request):
    if not request.user.is_authenticated:
        return redirect('adopter_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adopter_changepassword.html', d)


def ngo_changepassword(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    error = ""
    if request.method == "POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'ngo_changepassword.html', d)


def adopter_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Adopter.objects.get(user=user)
                if user1.type == "Adopter":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'adopter_login.html', d)


def adopter_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Adopter.objects.create(user=user, mobile=con, image=i, gender=gen, type="Adopter")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adopter_signup.html', d)


def adopter_petlist(request):
    if not request.user.is_authenticated:
        return redirect('adopter_login')
    pet = Pet.objects.all().order_by('-post_date')
    user = request.user
    adopter = Adopter.objects.get(user=user)
    data = Buy.objects.filter(adopter=adopter)
    li = []
    for i in data:
        li.append(i.pet.id)
    d = {'pet': pet, 'li': li}
    return render(request, 'adopter_petlist.html', d)





def donor_list(request):
    if not request.user.is_authenticated:
        return redirect('adopter_login')
    data = Donor.objects.all()
    d = {'data': data}
    return render(request, 'donor_list.html', d)


def shown_interest(request, pid):
    if not request.user.is_authenticated:
        return redirect('adopter_login')
    error = ""
    user = request.user
    adopter = Adopter.objects.get(user=user)
    pet = Pet.objects.get(id=pid)
    if request.method == 'POST':
        cl = request.POST['interest']
        Buy.objects.create(pet=pet, adopter=adopter, interest=cl, applydate=date.today())
        error = "done"
    d = {'error': error}
    return render(request, 'shown_interest.html', d)


def pet_details(request, pid):
    pet = Pet.objects.get(id=pid)
    d = {'pet': pet}
    return render(request, 'pet_details.html', d)


def adopter_details(request, pid):
    adopter = Adopter.objects.get(id=pid)
    buy = Buy.objects.get(id=pid)
    pet = Pet.objects.get(id=pid)
    d = {'adopter': adopter, 'buy': buy, 'pet': pet}
    return render(request, 'adopter_details.html', d)


def adopter_home(request):
    if not request.user.is_authenticated:
        return redirect('adopter_login')
    user = request.user
    adopter = Adopter.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        adopter.user.first_name = f
        adopter.user.last_name = l
        adopter.mobile = con
        adopter.gender = gen

        try:
            adopter.save()
            adopter.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            adopter.image = i
            adopter.save()
            error = "no"
        except:
            pass
    d = {'adopter': adopter, 'error': error}

    return render(request, 'adopter_home.html', d)


def Logout(request):
    logout(request)
    return redirect('home')


def ngo_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user:
            try:
                user1 = Ngo.objects.get(user=user)
                if user1.type == "NGO":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"
            except:
                error = "yes"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'ngo_login.html',d)

def ngo_signup(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        i = request.FILES['image']
        p = request.POST['pwd']
        e = request.POST['email']
        con = request.POST['contact']
        gen = request.POST['gender']
        reg = request.POST['reg']
        ngo = request.POST['ngoname']
        try:
            user = User.objects.create_user(first_name=f, last_name=l, username=e, password=p)
            Ngo.objects.create(user=user, mobile=con, image=i, ngo_name=ngo,reg_id=reg,gender=gen, type="NGO")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'ngo_signup.html',d)

def ngo_home(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    user = request.user
    ngo = Ngo.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        con = request.POST['contact']
        gen = request.POST['gender']

        ngo.user.first_name = f
        ngo.user.last_name = l
        ngo.mobile = con
        ngo.gender = gen

        try:
            ngo.save()
            ngo.user.save()
            error = "no"
        except:
            error = "yes"

        try:
            i = request.FILES['image']
            ngo.image = i
            ngo.save()
            error = "no"
        except:
            pass
    d = {'ngo': ngo, 'error': error}
    return render(request, 'ngo_home.html',d)

def ngo_fund(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        amp = request.POST['amount']
        try:
            Fundrais.objects.create(fname=f, lname=l, mobile=c, amount=amp, fundraisingdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error': error}

    return render(request, 'ngo_fund.html',d)


def ngo_pay(request):
    if not request.user.is_authenticated:
        return redirect('ngo_login')
    fund = Fundrais.objects.all()
    d = {'fund': fund}
    return render(request, 'ngo_pay.html',d)


def pet_wellfare(request):
    pet = Pet.objects.all().order_by('-post_date')
    d = {'pet': pet}
    return render(request, 'pet_wellfare.html', d)

def ngo_pet_details(request,pid):
    pet = Pet.objects.get(id=pid)
    d = {'pet': pet}
    return render(request, 'ngo_pet_detail.html', d)


