from django.shortcuts import render

# Create your views here.

def main_menu(request):
    return render(request, 'fourth_task/main_menu.html')

def shop(request):
    games = ['Atomic Heart', 'Cyberpunk 2077', 'PayDay2']
    context = {
        'games' : games
    }
    return render(request, 'fourth_task/shop.html',context)

def cart(request):
    return render(request, "fourth_task/cart.html")