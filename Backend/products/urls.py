from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('categories/', views.category_list, name='category_list' ),
    path('subcategory/', views.subcategory_list, name='subcategory_list'),
    path('filters/', views.filter_metadata, name='filter_metadata'),
    path('send-otp/', views.send_otp, name="send_otp"),
    path('verify-otp/', views.verify_otp, name="verify_otp"),
]
