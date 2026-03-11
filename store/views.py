from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Product, Category, Cart, CartItem


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    query = request.GET.get("search")

    if query:
        products = products.filter(name__icontains=query)

    
    category_products = {}

    for category in categories:
        filtered = products.filter(category=category)
        if filtered.exists():
            category_products[category] = filtered

    return render(request, "home.html", {
        "category_products": category_products,
        "query": query
    })
def add_to_cart(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    product = get_object_or_404(Product, id=id)
    quantity = int(request.POST.get("quantity", 1))

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not item_created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    return redirect("cart")

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect("home")

    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum([item.total_price() for item in items])

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


def remove_from_cart(request, id):
    if not request.user.is_authenticated:
        return redirect("home")

    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, id=id, cart=cart)
    item.delete()
    return redirect("cart")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("home")

    return render(request, "signup.html")

def user_logout(request):
    logout(request)
    return redirect("home")

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=id)[:4]

    return render(request, "product_detail.html", {
        "product": product,
        "related_products": related_products
    })
def checkout(request):
    return render(request, 'checkout.html')