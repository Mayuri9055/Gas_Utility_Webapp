
from django.urls import path
from gasbookapp import views
from gasbookapp.views import SimpleView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    path('home',views.home),
    path('home2',views.home2),
    path('catfilter/<cv>',views.catfilter),
    path('registration',views.registration),
    path('login',views.login_user),
    path('logout',views.user_logout),
    path('cart',views.cart),
    path('pd/<pid>',views.product_detail),
    path('addtocart/<pid>',views.addtocart),
    path('remove/<cid>',views.remove),
     path('updateqty/<qv>/<cid>',views.updateqty),
     path('makepayment',views.makepayment),
     path('sendmail',views.sendusermail),

    path('po',views.place_order),
    path('gasbooking',views.gasbooking),
    
    path('myview',SimpleView.as_view()),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
