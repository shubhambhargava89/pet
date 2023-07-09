from happytales import forms
from happytales.forms import LoginForm
from django.contrib import auth
from django.urls import path
from happytales import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordConfirmForm, MyPasswordResetForm,feedbackForm
from django.contrib import admin

urlpatterns = [
   
    path('', views.ProductView.as_view(), name="home"),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('customer', views.customer),
    path('orderplaced', views.orderplaced),
    path('carts', views.carts),
    path('product', views.product),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password__reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MyPasswordConfirmForm), name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('dog/', views.dog, name='dog'),
    path('dog/<slug:data>', views.dog, name='dogdata'),
    path('cat/', views.cat, name='cat'),
    path('cat/<slug:data>', views.cat, name='catdata'),
    path('dogfood/', views.dogfood, name='dogfood'),
    path('dogfood/<slug:data>', views.dogfood, name='dogfooddata'),
    path('catfood/', views.catfood, name='catfood'),
    path('catfood/<slug:data>', views.catfood, name='catfooddata'),


    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login' ),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('customerregistration/',views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('feedbacks/',views.Feedbacks.as_view(), name='feedbacks'),
    path('report/',views.Report.as_view(), name='report'),
# path('Signup/',views.Signup.as_view(), name='Signup'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/',views.payment_done, name='paymentdone'),
    path('accounts/donor_login/', views.donor_login, name='donor_login'),
    path('adopter_login', views.adopter_login, name='adopter_login'),
    path('donor_signup', views.donor_signup, name="donor_signup"),
path('donor_home', views.donor_home, name="donor_home"),
path('adopter_signup', views.adopter_signup, name="adopter_signup"),
path('adopter_home', views.adopter_home, name="adopter_home"),
path('add_pet', views.add_pet, name="add_pet"),
path('pet_list', views.pet_list, name="pet_list"),
path('adopter_petlist', views.adopter_petlist, name="adopter_petlist"),
path('delete_pet/<int:pid>', views.delete_pet, name="delete_pet"),
path('edit_pet/<int:pid>', views.edit_pet, name="edit_pet"),
path('adopter_list', views.adopter_list, name="adopter_list"),
path('donor_list', views.donor_list, name="donor_list"),
path('donor_changepassword', views.donor_changepassword, name="donor_changepassword"),
path('ngo_changepassword', views.ngo_changepassword, name="ngo_changepassword"),
path('adopter_changepassword', views.adopter_changepassword, name="adopter_changepassword"),
path('shown_interest/<int:pid>',views.shown_interest, name="shown_interest"),
path('pet_details/<int:pid>',views.pet_details, name="pet_details"),
path('adopter_details/<int:pid>',views.adopter_details, name="adopter_details"),
path('Logout', views.Logout, name="Logout"),
path('ngo_login', views.ngo_login, name='ngo_login'),
path('ngo_signup', views.ngo_signup, name='ngo_signup'),
path('ngo_home', views.ngo_home, name='ngo_home'),
path('ngo_fund', views.ngo_fund, name='ngo_fund'),
path('ngo_pay', views.ngo_pay, name='ngo_pay'),
path('pet_wellfare',views.pet_wellfare, name='pet_wellfare'),
path('ngo_pet_details/<int:pid>',views.ngo_pet_details, name='ngo_pet_details'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
