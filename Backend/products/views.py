# products/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, SubCategory, Brand, Size, Color, OTP
from .serializers import ProductSerializer, BrandSerializer, SizeSerializer, ColorSerializer
from django.core.mail import send_mail
from django.conf import settings

otp_store = {}
#@api_view(["GET"])
#def get_products(request):
#    products = Product.objects.all()
 #   serializer = ProductSerializer(products, many=True)
  #  return Response(serializer.data)

@api_view(['GET'])
def product_list(request):
    category_slug = request.GET.get('category')
    subcategory_slug = request.GET.get('subcategory')
    brand = request.GET.get('brand')
    size = request.GET.get('size')
    color = request.GET.get('color')
    sort_option = request.GET.get('sort')
    featured = request.GET.get('featured')
    
    products = Product.objects.all()
    
    #Filter by featured
    
    #if featured and featured.lower() == "true":
     #   products = products.filter(is_featured=True)

    # Filter by category
    if category_slug:
        products = products.filter(category__slug=category_slug)

    # Filter by subcategory
    if subcategory_slug:
        products = products.filter(subcategory__slug=subcategory_slug)
        
    # Filter by brand
    if brand:
        brand_list = brand.split(",")    
        products = products.filter(brand__name__in=brand_list)
        
    # Filter by size
    if size:
        size_list = size.split(",")
        products = products.filter(size__name__in=size_list)
    
    # Filter by color
    if color:
        color_list = color.split(",")
        products = products.filter(color__name__in=color_list)
            
            
        
    # Sorting
    
    if sort_option == "price_asc":
        products = products.order_by("price")
    elif sort_option == "price_dsc":
        products = products.order_by("-price")

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

        
        
@api_view(["GET"])
def category_list(request):
    categories = Category.objects.all()
    data = []

    for cat in categories:
        subcats = SubCategory.objects.filter(category=cat).values("name", "slug")
        
        featured_products = Product.objects.filter(category=cat, is_featured=True)[:3]
        featured_serialized = ProductSerializer(featured_products, many=True).data
        

        data.append({
            "name": cat.name,
            "slug": cat.slug,
            "subcategories": list(subcats),
            "featured_products": featured_serialized,
        })

    return Response(data)

@api_view(['GET'])
def subcategory_list(request):
    category_slug  = request.GET.get("category")
    
    if category_slug:
        subcategories = SubCategory.objects.filter(category__slug=category_slug)
        
    else:
        subcategories = SubCategory.objects.all()
        
    data = [
        {"id": sc.id, "name": sc.name, "slug": sc.slug}
        for sc in subcategories
    ]
    
    return Response(data)
    
    
@api_view(['GET'])
def filter_metadata(request):
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()
    
    return Response({
        "brands": BrandSerializer(brands, many=True).data,
        "sizes": SizeSerializer(sizes, many=True).data,
        "colors": ColorSerializer(colors, many=True).data,
    })
    
@api_view(['POST'])
def send_otp(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email required"}, status=400)
    
    #Create Otp
    otp_obj = OTP.objects.create(email=email)
    
    #Send email
@api_view(['POST'])
def send_otp(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email required"}, status=400)

    # Create OTP
    otp_obj = OTP.objects.create(email=email)

    try:
        # Send email (prints in console for development)
        send_mail(
            subject="Fashion Studio: Your Otp Code for Registration",
            message=f"Your OTP is {otp_obj.code}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception as e:
        return Response({"error": f"Failed to send OTP: {str(e)}"}, status=500)

    return Response({"message": "OTP sent Successfully"})


@api_view(['POST'])
def verify_otp(request):
    email = request.data.get("email")
    code = request.data.get("code")
    if not email or not code:
        return Response({"error": "Email and Code Required"}, status=400)
    
    try:
        otp_obj = OTP.objects.filter(email=email, code=code, verified=False).latest('created_at')
        if otp_obj.is_expired():
            return Response({"verified": False, "error": "OTP expired"})
        otp_obj.verified = True
        otp_obj.save()
        return Response({"verified": True})
    
    except OTP.DoesNotExist:
        return Response({"verified": False, "error": "Invalid OTP"})
    
    