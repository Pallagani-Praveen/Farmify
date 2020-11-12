from django.urls import path
from . import views as v
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',v.farmer_index,name="farmer_index"),
    path('add_crop/',v.add_crop,name='add_crop'),
    path('crop/<str:cropname>',v.related_crop,name='related_crop'),
    
] +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
