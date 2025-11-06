from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order
from django.contrib.auth import get_user_model 
User = get_user_model() 

# -----------------------------
# DASHBOARD HOME / INDEX
# -----------------------------
@login_required(login_url='users:login')
def index(request):
    orders_count = Order.objects.count()
    products_count = Product.objects.count()
    users_count = User.objects.count()
    
    recent_orders = Order.objects.all().order_by('-id')[:5]  # latest 5 orders
    recent_products = Product.objects.all().order_by('-id')[:5]  # latest 5 products

    context = {
        'orders_count': orders_count,
        'products_count': products_count,
        'users_count': users_count,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
    }
    return render(request, 'dashboard/index.html', context)

# -----------------------------
# PRODUCTS
# -----------------------------
@login_required(login_url='users:login')
def products(request):
    all_products = Product.objects.all()
    return render(request, 'dashboard/products.html', {'products': all_products})

@login_required(login_url='users:login')
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        Product.objects.create(name=name, price=price, stock=stock)
        messages.success(request, 'Product added successfully.')
        return redirect('dashboard:products')
    return render(request, 'dashboard/add_product.html')

@login_required(login_url='users:login')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('dashboard:products')
    return render(request, 'dashboard/edit_product.html', {'product': product})

@login_required(login_url='users:login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('dashboard:products')


# -----------------------------
# ORDERS
# -----------------------------
@login_required(login_url='users:login')
def orders(request):
    all_orders = Order.objects.all()
    return render(request, 'dashboard/orders.html', {'orders': all_orders})

@login_required(login_url='users:login')
def add_order(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, id=product_id)

        if quantity > product.stock:
            messages.error(request, 'Not enough stock.')
            return redirect('dashboard:add_order')

        Order.objects.create(customer_name=customer_name, product=product, quantity=quantity)
        product.stock -= quantity
        product.save()
        messages.success(request, 'Order created successfully.')
        return redirect('dashboard:orders')

    products = Product.objects.all()
    return render(request, 'dashboard/add_order.html', {'products': products})

@login_required(login_url='users:login')
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.customer_name = request.POST.get('customer_name')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity'))

        old_quantity = order.quantity
        product = get_object_or_404(Product, id=product_id)

        # Adjust stock
        product.stock += old_quantity
        if quantity > product.stock:
            messages.error(request, 'Not enough stock.')
            return redirect('dashboard:edit_order', order_id=order.id)
        product.stock -= quantity
        product.save()

        order.product = product
        order.quantity = quantity
        order.save()
        messages.success(request, 'Order updated successfully.')
        return redirect('dashboard:orders')

    products = Product.objects.all()
    return render(request, 'dashboard/edit_order.html', {'order': order, 'products': products})

@login_required(login_url='users:login')
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.product.stock += order.quantity
    order.product.save()
    order.delete()
    messages.success(request, 'Order deleted successfully.')
    return redirect('dashboard:orders')


# -----------------------------
# USERS MANAGEMENT
# -----------------------------
@login_required(login_url='users:login')
def users(request):
    all_users = User.objects.all()
    return render(request, 'dashboard/users.html', {'users': all_users})

@login_required(login_url='users:login')
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'User added successfully.')
            return redirect('dashboard:users')
    return render(request, 'dashboard/add_user.html')

@login_required(login_url='users:login')
def edit_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user_obj.username = request.POST.get('username')
        password = request.POST.get('password')
        if password:
            user_obj.set_password(password)
        user_obj.save()
        messages.success(request, 'User updated successfully.')
        return redirect('dashboard:users')
    return render(request, 'dashboard/edit_user.html', {'user_obj': user_obj})

@login_required(login_url='users:login')
def delete_user(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.user == user_obj:
        messages.error(request, 'You cannot delete yourself.')
        return redirect('dashboard:users')
    user_obj.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('dashboard:users')
