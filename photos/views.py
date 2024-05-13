from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignupForm, LoginForm
from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request,"Welcome, Account is created")
            user = form.save(commit=False)
            user.save()
            return redirect('login')

    else:
        form = SignupForm()
    return render(request, 'photos/signup.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully !!")
                return redirect('/gallery/')
    form = LoginForm()
    return render(request, "photos/login.html", {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')


def gallery(request):
    if request.user.is_authenticated:
        user = request.user
        category = request.GET.get('category')
        if category == None:
            photos = Photo.objects.filter(category__user=user)    
        else:
            photos = Photo.objects.filter(category__name=category, category__user=user)
        categories = Category.objects.filter(user=user)    
        context = {'categories': categories, 'photos': photos}
        return render(request, "photos/gallery.html", context)
    else:
        return HttpResponseRedirect('/login/')
    


def viewPhoto(request, pk):
    if request.user.is_authenticated:
        photo = Photo.objects.get(id=pk)
        return render(request, "photos/photo.html", {'photo': photo})
    else:
        return HttpResponseRedirect('/login/')


def addPhoto(request):
    if request.user.is_authenticated:
        user = request.user
        categories = user.category_set.all()
        if request.method == "POST":
            data = request.POST
            images = request.FILES.getlist('images')
            if data['category'] != 'none':
                category = Category.objects.get(id=data['category'])
            elif data['category_new'] != '':
                category, created = Category.objects.get_or_create(user=user, name=data['category_new'])
            else:
                category = None
            for image in images:
                photo = Photo.objects.create(
                    category = category,
                    description = data['description'],
                    image = image,
                    )
            return redirect('gallery')
        context = {'categories': categories}
        return render(request, "photos/add.html", context)
    return HttpResponseRedirect('/login/')
