from django.shortcuts import render

# Create your views here.

def main_menu(request):
    return render(request, 'third_task/main_menu.html')

def shop(request):
    return render(request, 'third_task/shop.html')

def cart(request):
    return render(request, "third_task/cart.html")