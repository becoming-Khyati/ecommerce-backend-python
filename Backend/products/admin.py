from django.contrib import admin
from .models import Product
from .models import Category, SubCategory, Brand, Size, Color
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Brand)
admin.site.register(Size)
admin.site.register(Color)