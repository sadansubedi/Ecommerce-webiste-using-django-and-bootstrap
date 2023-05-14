from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . forms import MyPasswordResetForm,MySetPasswordForm
from django.contrib.auth import views as auth_views
from app import views
urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='payment_done'),
    
    path('cart/',views.Show_cart,name="showcart"),
    path('pluscart/',views.Plus_cart),
    path('minuscart/',views.Minus_cart),
    path('removecart/',views.Remove_cart,name="removecart"),

    
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
#-----this below url are for reset password by email in 4 step (PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView) no need to inheritate it,like others ok--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),#here MyPasswordResetForm class contain email field in forms.py from where user send in their own email account 
    path('passwordreset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'), #here  it messages that email is sent to respective email ok 
    path('passwordreset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'), #after entering password and confirm password and save it ok MySetPasswordForm inheritance from forms.py
    path('passwordreset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'), #here  it messages that you have successfully change the forget password ok 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),#here slug is becoz of string ok i.e samsung or real me and its priority is high rather than that data=none ok
    path('account/login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
]+ static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)
