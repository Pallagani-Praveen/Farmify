from django.urls import path,include
from . import views as v
urlpatterns = [
    path('',v.dealer_index,name="dealer_index"),
    path('all_crops',v.get_all_crops,name='get_all_crops'),
    path('crop_eval',v.crop_eval,name='crop_eval'),
]