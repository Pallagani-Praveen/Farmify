from django.shortcuts import redirect, render,HttpResponse
from farmify.mongoClient import MongoClient
from bson.objectid import ObjectId
from numpy import std,mean
from farmers.models import PinToLatLong
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auths.models import User
from statistics import mean,stdev

client = MongoClient().getConnection()

# Create your views here.
@login_required(login_url='/auth/login')
def dealer_index(request):
    deals = list(client.Farmify.dealers_deals.find({'user':request.user.email}))
    farmer_requested_deals = list(client.Farmify.farmer_request_dealer.find({'dealer':request.user.email}))
    for deal in deals:
        deal['timestamp'] = deal['_id'].generation_time
        deal['id'] = deal['_id']
        temp_reqs = []
        for farmer_req in farmer_requested_deals:
            if ObjectId(farmer_req['deal_id']) == deal['_id']:
                temp_reqs.append(farmer_req)
        deal['readyfarmers'] = len(temp_reqs)
        
        

            
       
    context = {'deals':deals}
    return render(request,'dealers/dealer_index.html',context=context)

@login_required(login_url='/auth/login')
def add_deal(request):
    if request.user.role == 'farmer':
        messages.warning(request,'Action Not Allowed')
        return redirect('/')

    if request.method == 'POST':
        cropname = request.POST['cropname']
        start_size = request.POST['start_size']
        end_size = request.POST['end_size']
        metric = request.POST['metric']
        price = request.POST['price']

        state = request.POST['state']
        pincode = request.POST['pincode']
        area = request.POST['area']
        phone = request.POST['phone']

        doc = dict()
        doc['user'] = request.user.email
        doc['cropname'] = cropname
        doc['start_size'] = start_size
        doc['end_size'] = end_size
        doc['metric'] = metric
        doc['price'] = price
        doc['state'] = state
        doc['pincode'] = pincode
        doc['area'] = area
        doc['phone'] = phone

        client.Farmify.dealers_deals.insert(doc)
        return redirect('/dealers/')

    return render(request,'dealers/add_deal.html')


def get_all_crops(request):
    crops = list(client.Farmify.farmers_crops.find())
    for crop in crops:
        crop['id'] = crop['_id']
        crop['timestamp'] = crop['_id'].generation_time
    context = {'crops':crops}
    return render(request,'dealers/all_crops.html',context=context)

def crop_eval(request):
    def eval_per_unit_price(crop):
        return int(crop['price'])/int(crop['size'])
    if 'crop_id' not in request.GET:
        return redirect('/')

    cropid = request.GET['crop_id']
    crop = list(client.Farmify.farmers_crops.find({'_id':ObjectId(cropid)}))[0]
    crops = list(client.Farmify.farmers_crops.find({'cropname':crop['cropname']}))

    per_unit_prices = list(map(eval_per_unit_price,crops))
    mu,sd = mean(per_unit_prices),std(per_unit_prices)

    if mu-sd <= eval_per_unit_price(crop) <= mu+sd:
        color = 'success'
        sugg = 'Go'
    elif (mu-2*sd) <= eval_per_unit_price(crop) <= (mu+2*sd):
        color = 'primary'
        sugg = 'Think'
    else:
        color = 'danger'
        sugg = 'No'

    if PinToLatLong.objects.filter(pin=int(crop['pincode'])).count()!=0:
        pintolatlong = PinToLatLong.objects.filter(pin=int(crop['pincode']))[:1].get()
        lat = pintolatlong.lat
        long = pintolatlong.long
        area = crop['area']
    else:
        lat = 18.4435
        long = 83.546
        area = 'Undetermined'

    context = {'crop':crop,'crops':crops,'mu':mu,'sd':sd,'cropname':crop['cropname'],'color':color,'sugg':sugg,'lat':lat,'long':long,'area':area}
    return render(request,'dealers/crop_eval.html',context=context)

@login_required(login_url='/auth/login')
def dealer_profile(request,user=None):
    user += '@gmail.com'
    user = User.objects.get(email=user)
    return HttpResponse('Dealer Profile Page is Yet to build')

@login_required(login_url='/auth/login')
def deal_details(request):
    if 'deal_id' not in request.GET:
        messages.warning(request,'Action Not Allowed')
        return redirect('/')

    deal_id = request.GET['deal_id']
    farmers = list(client.Farmify.farmer_request_dealer.find({'deal_id':deal_id}))
    deal = list(client.Farmify.dealers_deals.find({'_id':ObjectId(deal_id)}))[0]
    all_deal_crops = list(client.Farmify.farmers_crops.find({'cropname':deal['cropname']}))
    prices = list(map(lambda x: int(x['price'])/int(x['size']),all_deal_crops))
    mu,sd = mean(prices),stdev(prices)
    deal_price_range = {'start':int(deal['price'])/int(deal['end_size']),'end':int(deal['price'])/int(deal['start_size'])}
    context = {'deal':deal,'farmers':farmers,'mu':mu,'sd':sd,'deal_price_range':deal_price_range}
    return render(request,'dealers/deal_details.html',context=context)


    
