from django.shortcuts import render,HttpResponseRedirect,redirect
from . models import Customer,Cart,Product,OrderPlaced
from django.views import View
from . forms import CustomerRegistrationForm,LoginForm,MyPasswordChangeForm,CustomerProfileForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):  #getting data from DB
  totalitem =0 
  mobiles = Product.objects.filter( category='M')
  laptops = Product.objects.filter( category='L')
  topwears= Product.objects.filter( category='TW')
  bottomwears = Product.objects.filter( category='BW')#here it filter from model.py,there is a category named field ok 
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'mobiles':mobiles,'laptops':laptops,'bottomwears':bottomwears,'topwears':topwears,'totalitem':totalitem})

class ProductDetailView(View):
 def get(self,request,pk):
  totalitem =0 
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    print(item_already_in_cart)
  return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
 
def add_to_cart(request):
  if request.user.is_authenticated:
    user= request.user  # request.user means login user 
    product_id = request.GET.get('prod_id')# i even dont know how prod_id come but i know it comes from productdetails.html (hiddenform) remember it haha http://127.0.0.1:8000/add-to-cart/?prod_id=19 later i think it comes from url like whenever user click on add-to-cart it generate in url as prod_id =value ok  
    #print(product_id) # or we can understand by this as well (when we try to access through name i.e name="prod_id" we get the value i.e value="{{product.id}}" from productdetails.html line no 17)
    product = Product.objects.get(id=product_id) #here searching the product_id in DB
    Cart(user=user,product=product).save()
    return redirect('/cart') #that means to show_cart tira
  else:
    return HttpResponseRedirect('/account/login/')


def Show_cart(request):
  totalitem =0 
  if request.user.is_authenticated:
    totalitem =len(Cart.objects.filter(user=request.user))
    user = request.user
    cart =Cart.objects.filter(user=user)
    #print(cart)#it return queryset
    amount = 0.0
    shipping_charge = 80
    Total_amount = 0.0
    cart_product =[p for p in Cart.objects.all() if p.user == user]#list-compression where p in Cart.objects.all() get all data from Cart and store in p and if p.user and user equal then data flow from p to cart_product as list datatype ok
    #print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount =(p.quantity*p.product.discounted_price) #p.product.discounted_price is possible bcoz of one to many relation betwn Cart and Product in DB 
        amount += tempamount
        Total_amount = amount + shipping_charge
      return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':Total_amount,'amount':amount,'totalitem':totalitem})
    else:# if user still dont cart any item then show them empty page ok
      return render(request, 'app/empty.html')
  else:
      return HttpResponseRedirect('/account/login/')
    
#if you want to add more same item we click in (+) so that it increase number of quantity ok for this 
def Plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id'] #here prod_id are get from myscript.js where  prod_id:id is ok
    c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user)) # to know about Q  below the code we describe it ok 
    c.quantity += 1
    c.save()
    amount = 0.0
    shipping_charge = 80
    Total_amount = 0.0
    cart_product =[p for p in Cart.objects.all() if p.user == request.user]#list-compression where p in Cart.objects.all() get all data from Cart and store in p and if p.user and user equal then data flow from p to cart_product as list datatype ok
    #print(cart_product)
    for p in cart_product:
        tempamount =(p.quantity*p.product.discounted_price) #p.product.discounted_price is possible bcoz of one to many relation betwn Cart and Product in DB 
        amount += tempamount
        Total_amount = amount + shipping_charge

    data ={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':Total_amount
    }
    return JsonResponse(data) #this data goes to myscript.js and execute success function ok
      
def Minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id'] #here prod_id are get from myscript.js where  prod_id:id is ok
    c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user)) # to know about Q  below the code we describe it ok 
    c.quantity -=1
    c.save()
    amount = 0.0
    shipping_charge = 80
    Total_amount = 0.0
    cart_product =[p for p in Cart.objects.all() if p.user == request.user]#list-compression where p in Cart.objects.all() get all data from Cart and store in p and if p.user and user equal then data flow from p to cart_product as list datatype ok
    #print(cart_product)
    for p in cart_product:
        tempamount =(p.quantity*p.product.discounted_price) #p.product.discounted_price is possible bcoz of one to many relation betwn Cart and Product in DB 
        amount += tempamount
        Total_amount = amount + shipping_charge

    data ={
      'quantity':c.quantity,
      'amount':amount,
      'totalamount':Total_amount
    }
    return JsonResponse(data) #this data goes to myscript.js and execute success function ok

     
def Remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id'] #here prod_id are get from myscript.js where  prod_id:id is ok
    c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user)) # to know about Q  below the code we describe it ok 
    c.delete()
    amount = 0.0
    shipping_charge = 80
    Total_amount = 0.0
    cart_product =[p for p in Cart.objects.all() if p.user == request.user]#list-compression where p in Cart.objects.all() get all data from Cart and store in p and if p.user and user equal then data flow from p to cart_product as list datatype ok
    #print(cart_product)
    for p in cart_product:
        tempamount =(p.quantity*p.product.discounted_price) #p.product.discounted_price is possible bcoz of one to many relation betwn Cart and Product in DB 
        amount += tempamount
        Total_amount = amount + shipping_charge

    data ={
      'amount':amount,
      'totalamount':Total_amount
    }
    return JsonResponse(data) 

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
 op = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

def change_password(request):
   if request.user.is_authenticated:
        if request.method == 'POST':
            form = MyPasswordChangeForm(user=request.user,data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request,form.user) #without it after password change it automaticatically logout but i said to login and goes to profile
                return HttpResponseRedirect('/profile/')
        else:
            form = MyPasswordChangeForm(user=request.user)
        return render(request,'app/changepassword.html',{'form':form})
   else:
      return HttpResponseRedirect('/account/login/')
 

def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category ='M') #here category came from db of class Product
 elif data == 'Samsung' or data == 'OPPO':
    mobiles = Product.objects.filter(category='M').filter(brand=data) #here brand came from db of class Product 
 elif data == 'below':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__lt = 30000) #here __lt means less than ok
 elif data == 'above':
    mobiles = Product.objects.filter(category='M').filter(discounted_price__gt = 30000) #here __gt means greater than ok
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

#def login(request):
 #return render(request, 'app/login.html')
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    #messages.success(request,'Logged in Successfully')
                    return HttpResponseRedirect('/profile/')
        else:
            form = LoginForm()
        return render(request,'app/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/profile/')

def user_logout(request):
   logout(request)
   return HttpResponseRedirect('/account/login/')
   

class CustomerRegistrationView(View):
   def get(self,request): #getting BLANK form from DB
    form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html',{"form":form})

   def post(self,request):     #getting data form from user and save in DB 
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
     messages.success(request,'Congratulations !! Registered Successfully')
     form.save()
     form = CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html',{"form":form})
    

def checkout(request):
 if not request.user.is_authenticated:
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.00
    shipping_charge = 80.0
    Total_amount = 0.0
    cart_product =[p for p in Cart.objects.all() if p.user == request.user]#list-compression where p in Cart.objects.all() get all data from Cart and store in p and if p.user and user equal then data flow from p to cart_product as list datatype ok
    if cart_product:
      for p in cart_product:
            tempamount =(p.quantity*p.product.discounted_price) #p.product.discounted_price is possible bcoz of one to many relation betwn Cart and Product in DB 
            amount += tempamount
      Total_amount = amount + shipping_charge
    return render(request, 'app/checkout.html',{'add':add,'totalamount':Total_amount,'cart_items':cart_items})
 else:
   return HttpResponseRedirect('/account/login/')
     
   

@login_required
def payment_done(request):
  user = request.user
  custid =request.GET.get('custid') #when we try to access through name i.e name="custid" we get the value i.e value="{{add.id}}" from checkout.html line no 34
  print(custid)
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return redirect('orders')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form = CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      usr = request.user
      name = form.cleaned_data['name']#['name']are get from form.py ok  
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode) #here Customer is model ok and we are passing data from form.py to model.py
      reg.save()
      form = CustomerProfileForm() #after submitting form,data goes to model and here form again become blanks
      messages.success(request,'Congratulations !! Profile Updated Successfully')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'}) 

      
'''
why we use update_session_auth_hash function?
=> When a user logs in, Django creates a session for that user and sets a session ID in the user's browser. This session ID is then used to identify the user in subsequent requests. However, if an attacker is able to obtain the session ID before the user logs in, they can use that session ID to hijack the user's session.
To prevent session fixation attacks, Django provides the (update_session_auth_hash function). This function takes two arguments: the current request and the user whose session needs to be updated. It updates the session hash by creating a new random value and associating it with the user's session, which invalidates any previous session IDs.

what is the use of Q and why we import it ?
#In Django, Q is a class that is used to build complex queries for database lookups using the filter() or exclude() methods of a QuerySet.
Using Q objects, you can combine multiple conditions using logical operators (such as & for AND and | for OR) and parentheses to group conditions.
In your example, Q(product=prod_id) & Q(user=request.user) creates a Q object that represents a filter condition with two conditions combined by the & operator. The first condition is product=prod_id, which filters the Cart objects where the product field matches the value of prod_id. 
The second condition is user=request.user, which filters the Cart objects where the user field matches the current user.

'''