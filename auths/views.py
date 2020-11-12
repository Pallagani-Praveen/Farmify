from auths.models import User
from django.shortcuts import redirect, render,HttpResponse
from auths.forms import UserCreationFrom,UserLoginForm
from auths.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

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
        else:
            messages.warning(request,'Invalid Input To The Form')
    context = {'form':form}
    return render(request,'auths/signup.html',context=context)

def auths_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    next = request.GET.get('next')
    
    form = UserLoginForm()
    if request.method=='POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            next = request.POST['next']
            if User.objects.filter(email=email).count() == 1:
                if User.objects.get(email=email).role != role:
                    messages.error(request,'Invalid Role Given')
                    return redirect('/auth/login')
                user = authenticate(email=email,password=password,role=role)
                if user:
                    login(request,user)
                    if next!='None':
                        return redirect(next)
                    return redirect('landing_page')
            else:
                messages.error(request,'Invalid Email/Password')
        else:
            messages.warning(request,'Invalid User Infomation')

    context = {'form':form,'next':next}
    return render(request,'auths/login.html',context=context)


def auths_logout(request):
    logout(request)
    return redirect('landing_page')

