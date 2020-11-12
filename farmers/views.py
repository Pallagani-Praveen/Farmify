from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,HttpResponse
from farmify.mongoClient import MongoClient
from django.contrib import messages
from bson.objectid import ObjectId


client = MongoClient().getConnection()

# Create your views here.

def farmer_index(request):
    crops = list(client.Farmify.farmers_crops.find({'user':request.user.email}))
    for crop in crops:
        crop['timestamp'] = crop['_id'].generation_time
       
    context = {'crops':crops}
    return render(request,'farmers/farmer_index.html',context=context)

@login_required(login_url='/auth/login')
def add_crop(request):
    if request.user.role == 'dealer':
        messages.warning(request,'Action Not Allowed')
        return redirect('/')
    if request.method == 'POST':
        cropname = request.POST['cropname']
        size = request.POST['size']
        metric = request.POST['metric']
        price = request.POST['price']

        state = request.POST['state']
        pincode = request.POST['pincode']
        area = request.POST['area']
        phone = request.POST['phone']

        doc = dict()
        doc['user'] = request.user.email
        doc['cropname'] = cropname
        doc['size'] = size
        doc['metric'] = metric
        doc['price'] = price
        doc['state'] = state
        doc['pincode'] = pincode
        doc['area'] = area
        doc['phone'] = phone

        client.Farmify.farmers_crops.insert(doc)
        return redirect('/farmers/')
    return render(request,'farmers/add_crop.html',context={})

@login_required(login_url='/auth/login')
def related_crop(request,cropname):
    user_crops = list(client.Farmify.farmers_crops.find({'user':request.user.email,'cropname':cropname}))
    related_crops = list(client.Farmify.farmers_crops.find({'cropname':cropname,'user':{'$not':{'$regex':request.user.email}}}))
    for crop in related_crops:
        crop['timestamp'] = crop['_id'].generation_time
    return render(request,'farmers/related_crops.html',context={'user_crops':user_crops,'cropname':cropname,'related_crops':related_crops})

