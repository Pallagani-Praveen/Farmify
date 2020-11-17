from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,HttpResponse
from farmify.mongoClient import MongoClient
from django.contrib import messages
from bson.objectid import ObjectId
from auths.models import User



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

@login_required(login_url='/auth/login')
def get_all_deals(request):

    if client==None:
        return redirect('/')

    deals = list(client.Farmify.dealers_deals.find({}))
    farmer_requested_dealer_deals = list(client.Farmify.farmer_request_dealer.find({"farmer":request.user.email}))
    
    for deal in deals:
        deal['img'] = User.objects.get(email=deal['user']).avatar
        deal['timestamp'] = deal['_id'].generation_time
        deal['id'] = deal['_id']
        deal['status'] = 'request'
        for request_deal in farmer_requested_dealer_deals:
            if deal['id'] == ObjectId(request_deal['deal_id']):
                deal['status'] = request_deal['status']
        
        
    context = {'deals':deals}
    return render(request,'farmers/all_deals.html',context=context)

@login_required(login_url='/auth/login')
def request_dealer_deal(request):
    if request.method == 'POST':
        farmer = request.POST['farmer']
        dealer = request.POST['dealer']
        deal_id = request.POST['deal_id']
        status = 'waiting'
        doc = dict()
        doc['farmer'] = farmer
        doc['dealer'] = dealer
        doc['deal_id'] = deal_id
        doc['status'] = status
        res = client.Farmify.farmer_request_dealer.insert(doc)
        print(type(ObjectId))
        if type(res)==type(ObjectId(res)):
            return HttpResponse('success')
        else:
            return HttpResponse('Error')
    return redirect('/')



