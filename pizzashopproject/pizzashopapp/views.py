from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Pizza
from .forms import *


# Create your views here.
def home(request):
    return redirect(pizzashop_home)


@login_required(login_url='/pizzashop/sign-in/')
def pizzashop_home(request):
    return redirect(pizzashop_pizza)


@login_required(login_url='/pizzashop/sign-in/')
def pizzashop_account(request):
    user_form = UserFormFormEdit(instance=request.user)
    pizzashop_form = PizzaShopForm(instance=request.user.pizzashop)

    if request.method == "POST":
        user_form = UserFormFormEdit(request.POST, instance=request.user)
        pizzashop_form = PizzaShopForm(request.POST, request.FILES, instance=request.user.pizzashop)

        if user_form.is_valid() and pizzashop_form.is_valid():
            user_form.save()
            pizzashop_form.save()

    return render(request, 'pizzashop/account.html', {
        'user_form': user_form,
        'pizzashop_form': pizzashop_form
    })


@login_required(login_url='/pizzashop/sign-in/')
def pizzashop_pizza(request):
    pizzas = Pizza.objects.filter(pizzashop=request.user.pizzashop).order_by("-id")
    return render(request, 'pizzashop/pizza.html', {
        'pizzas': pizzas,
    })


@login_required(login_url='/pizzashop/sign-in/')
def pizzashop_add_pizza(request):
    form = PizzaForm()
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.pizzashop = request.user.pizzashop
            pizza.save()
            return redirect(pizzashop_pizza)
    return render(request, 'pizzashop/add_pizza.html', {
        'form':  form,
    })


@login_required(login_url='/pizzashop/sign-in/')
def pizzashop_edit_pizza(request, pizza_id):
    form = PizzaForm(instance=Pizza.objects.get(id=pizza_id))
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance=Pizza.objects.get(id=pizza_id))
        if form.is_valid():
            pizza = form.save()
            return redirect(pizzashop_pizza)

    return render(request, 'pizzashop/edit_pizza.html', {
        'form':  form,
    })


def pizzashop_sign_up(request):
    user_form = UserForm()
    pizzashop_form = PizzaShopForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        pizzashop_form = PizzaShopForm(request.POST, request.FILES)

        if user_form.is_valid() and pizzashop_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_pizzashop = pizzashop_form.save(commit=False)
            new_pizzashop.owner = new_user
            new_pizzashop.save()

            login(request, authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            ))

            return redirect(pizzashop_home)

    return render(request, 'pizzashop/sign_up.html', {
        'user_form': user_form,
        'pizzashop_form': pizzashop_form
    })

