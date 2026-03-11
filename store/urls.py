from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart'),
     path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.user_logout, name="logout"),
    path('remove/<int:id>/', views.remove_from_cart, name="remove_from_cart"),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
]

