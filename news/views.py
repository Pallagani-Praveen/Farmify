from django.shortcuts import render,HttpResponse
import requests as req
from farmify.mongoClient import MongoClient
from .newsStructure import News
# Create your views here.

def news_index(request):
    newsKey = MongoClient().getNewsKey()
    res = req.get('http://newsapi.org/v2/top-headlines?country=in&apiKey='+newsKey)
    if res.status_code == 200:
        news = res.json()['articles']
        news = map(News,news)
    else:
        news = 'News Not Found'
    context = {'news':news}
    return render(request,'news/news_index.html',context=context)


