from rest_framework import serializers
from .models import Product, Category, SubCategory, Brand, Size, Color

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields =['id', 'name', 'logo']
        
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name', 'hex_code']
        
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    subcategory = serializers.StringRelatedField()
    brand = BrandSerializer()
    size = SizeSerializer()
    color = ColorSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'description', 'category', 'subcategory', 'brand', 'size', 'color', 'is_featured']
