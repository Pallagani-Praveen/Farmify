from auths.models import User
from django.shortcuts import redirect, render,HttpResponse
from auths.forms import UserCreationFrom,UserLoginForm
from auths.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def authindex(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request,'auths/auth_index.html',context=context)

def auths_signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserCreationFrom()
    if request.method == 'POST':
        form = UserCreationFrom(request.POST,request.FILES)
        if form.is_valid():
            print(request.FILES,request.POST)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            second_name = form.cleaned_data['second_name']
            avatar = form.cleaned_data['avatar']
            gender = form.cleaned_data['gender']
            role = form.cleaned_data['role']
            user = User(email=email,first_name=first_name,second_name=second_name,avatar=avatar,gender=gender,role=role)
            user.set_password(password)
            user.save()
            return redirect('/auth/')
    context = {'form':form}
    return render(request,'auths/signup.html',context=context)

def auths_login(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = UserLoginForm()
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            user = authenticate(email=email,password=password,role=role)
            if user:
                login(request,user)
                return redirect('landing_page')

    context = {'form':form}
    return render(request,'auths/login.html',context=context)


def auths_logout(request):
    logout(request)
    return redirect('landing_page')

