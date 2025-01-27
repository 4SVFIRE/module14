from django.shortcuts import render
from .forms import UserRegister
from django.http import HttpResponse

users = ['fire', 'admin', 'dyrak']

def sign_up_by_django(request):
    info = {}
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            age = form.cleaned_data['age']

            error = None

            if password != repeat_password:
                error = "Пароли не совпадают!"
            elif age < 18:
                error = "Возраст должен быть не менее 18 лет!"
            elif username in users:
                error = "Пользователь уже существует!"

            if error:
                info['error'] = error
                info['form'] = form  # Передаем форму в контекст
                return render(request, 'fifth_task/registration_page.html', info)

            users.append(username)
            return HttpResponse(f"Приветствуем, {username}!")

        info['form'] = form
    else:
        info['form'] = UserRegister()

    return render(request, 'fifth_task/registration_page.html', info)


def sign_up_by_html(request):
    info = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        repeat_password = request.POST.get("repeat_password")
        age = int(request.POST.get("age"))

        error = None
        if password != repeat_password:
            error = "Пароли не совпадают!"
        elif age < 18:
            error = "Возраст должен быть не менее 18!"
        elif username in users:
            error = "Пользователь уже существует!"

        if error:
            info["error"] = error
            return render(request, "fifth_task/registration_page.html", info)
        else:
            users.append(username)
            return HttpResponse(f"Приветствуем, {username}!")

    return render(request, "fifth_task/registration_page.html", info)