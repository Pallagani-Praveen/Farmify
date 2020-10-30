from django.shortcuts import render,HttpResponse

def landing_view(request):
    return render(request,'farmify/index.html')