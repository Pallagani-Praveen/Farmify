from django.shortcuts import redirect, render,HttpResponse
from farmify.mongoClient import MongoClient
from bson.objectid import ObjectId
from numpy import std,mean
from farmers.models import PinToLatLong

client = MongoClient().getConnection()

# Create your views here.
def dealer_index(request):
    return HttpResponse('Dealer Index Page')

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
    
