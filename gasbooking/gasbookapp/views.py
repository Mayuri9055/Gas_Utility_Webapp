from django.shortcuts import render,HttpResponse,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from gasbookapp.models import Product,Cart,Order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.
# def home(request):
#     #return HttpResponse("this is about page")
#     return render(request,'hello.html')
def home(request):
    context={}
    p=Product.objects.filter(is_active=True)
    print(p)
    print(p[0])
    print(p[0].price)
    print(p[0].cat)
    context['products']=p
    return render(request,'index.html',context)
def home2(request):
    context={}
    p=Product.objects.all()
    context['products']=p
    return render(request,'index.html',context)
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=Product.objects.filter(q1&q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)    
def registration(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname'] 
        upass=request.POST['upass'] 
        ucpass=request.POST['ucpass']
        if uname=="" or upass=="" or ucpass=="":
           context['errmsg']="field cannot empty"
           return render(request,'registration.html',context)
        elif upass!=ucpass:
            context['errmsg']="password and confirm password does not match"
            return render(request,'registration.html',context)
        else:
            try:
               u=User.objects.create(username=uname,email=uname)
               u.set_password(upass)
               u.save()
               context['success']="user created successfully"
               return render(request,'registration.html',context)
            except Exception:
                context['errmsg']="user with same username already excit"
                return render(request,'registration.html',context)
    else:
        return render(request,'registration.html')
def login_user(request):
    context={}
    if request.method=='POST':
        uname=request.POST['uname'] 
        upass=request.POST['upass'] 
        if uname=="" or upass=="":
            context['errmsg']="field cannot be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)#start session and store id of logged in user session
                return redirect('/home')
            else:
                context['errmsg']="invalid username and password"
                return render(request,'login.html',context)
    return render(request,'login.html')
def user_logout(request):
    logout(request)
    # context={}
    # context['title1']="logout"
    #demo(request)
    #return render(request,'header.html',context)
    return redirect('/home')

def place_order(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    oid=random.randrange(1000,9999)
    print("order id:",oid)
    for x in c:
        # print(x)
        # print(x.pid)
        # print(x.uid)
        # print(x.qty)
        o=Order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    n=len(orders)
    for x in orders:
        s=s+x.pid.price*x.qty
    context={}
    context['products']=orders
    context['total']=s
    context['np']=n
    return render(request,'placeorder.html',context)
   

def product_detail(request,pid):
    context={}
    context['products']=Product.objects.filter(id=pid)
    return render(request,'productdetail.html',context)
def addtocart(request,pid):
    if request.user.is_authenticated:
        # print("user is logged")
        # return HttpResponse("user logged in")
        u=User.objects.filter(id=request.user.id)
        # print(u)
        # print(u[0])
        # print(u[0].username)
        # print(u[0].is_superuser)
        p=Product.objects.filter(id=pid)
        # print(p)#check product exist or not
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1&q2)
        print(c)
        n=len(c)
        print(n)
        context={}
        context['products']=p
        if n==1:
            context['msg']="product already exist!!"
        else:   
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="product added successfully to cart"
        return render(request,'productdetail.html',context)
    else:
        return redirect('/login')

   
def cart(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid)
    # print(c)
    # print(c[0])
    # print(c[1])
    # print(c[0].pid.name)
    # print(c[0].pid.price)
    n=len(c)
    s=0
    for x in c:
        #print(x)
        s=s+x.pid.price
    print(s)
    context={}
    context['np']=n
    context['total']=s
    context['products']=c
    return render(request,'cart.html',context)
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')
def updateqty(request,qv,cid):
    # print(type(qv))
    # return HttpResponse("in update quantity")
    c=Cart.objects.filter(id=cid)
    s=0
    # print(c)
    # print(c[0].qty)
    if qv=='1':
        t=c[0].qty+1
        c.update(qty=t)
    else:
        if c[0].qty>1:
            t=c[0].qty-1
            c.update(qty=t)
    for x in c:
        #print(x)
        s=s+x.pid.price*x.qty#s+800*5
    context={}
    # context['np']=n
    context['products']=c
    context['total']=s
    #return HttpResponse("in update quantity")
    #return redirect('/cart')
    return render(request,'cart.html',context)
def makepayment(request):
    orders=Order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_wMhTsDtW2in3XL", "JUwYPC3QFqNQSMmcSwW8k7bT"))
    data = { "amount": s*100, "currency": "MYR", "receipt": "oid" }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    context['data']=payment
    return render(request,'pay.html',context)
def sendusermail(request):
    uemail=request.user.email
    print(uemail)
    send_mail(
    "Ekart-Order placed successfuully",
    "Order details are:",
    "mayuridevkate74@gmail.com",
    [uemail],
    fail_silently=False,
)
    return HttpResponse("mail is send successfully")




def gasbooking(request):
    return render(request,'index.html')

#class based view 
class SimpleView(View):
    def get(self,request):
        return HttpResponse("hello simple view")
