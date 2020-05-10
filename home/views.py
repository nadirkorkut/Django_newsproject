from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import logout,login,authenticate
from django import forms
import json
from home.forms import SignUpForm


# Create your views here.
from home.models import Setting, ContactFormu,ContactFormMessage
from news.models import News,Category,Images,Comment
from home.forms import SearchForm

def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata=News.objects.all()[:15]
    category = Category.objects.all()
    daynews=News.objects.all()[:25]
    lastnews=News.objects.all().order_by('-id')[:5]
    randomnews = News.objects.all().order_by('?')[:3]


    context={"setting" : setting ,
             "category" : category ,
             'page':'home',
             'sliderdata':sliderdata,
             'daynews': daynews,
             'lastnews': lastnews,
             'randomnews' : randomnews
             }
    return render(request, 'index.html', context)

def hakkimizda(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context={'setting' : setting,
             'category' : category
             }
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context={'setting' : setting,
             'category' : category
             }
    return render(request, 'referanslarimiz.html', context)

def iletisim(request):
    if request.method == 'POST':
        form=ContactFormu(request.POST)
        if form.is_valid():
            data=ContactFormMessage()
            data.name=  form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,"Mesajınız Başarılı bir şekilde iletilmiştir.Teşekkür Ederiz.")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form=ContactFormu()
    category = Category.objects.all()
    context={"setting" : setting,
             'form' : form,
             'category' : category
             }
    return render(request, 'iletisim.html', context)

def category_news(request,id,slug):
    news=News.objects.filter(category_id=id)
    category=Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    context={'news': news,
             'category' : category,
             'slug' : slug,
             'categorydata' : categorydata,
             }
    return render(request,'news.html',context)

def news_detail(request,id,slug):
    category=Category.objects.all()
    new = News.objects.get(pk=id)
    images=Images.objects.filter(news_id=id)
    comments=Comment.objects.filter(news_id=id,status='True')
    context = {'new': new,
               'category': category,
               'images': images,
               'comments' : comments,
               }
    return render(request,'news_detail.html',context)

def news_search(request):
    if request.method == 'POST': #Check Form post
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['query'] #get form data
            catid = form.cleaned_data['catid']

            if catid == 0:
                news = News.objects.filter(title__icontains=query) #select * from news where title like %query%
            else:
                news =News.objects.filter(title__icontains=query,category_id=catid)
            context ={ 'news': news,
                       'category': category,

                     }
            return render(request, 'news_search.html', context)
    return HttpResponseRedirect('/')

def news_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        news = News.objects.filter(title__icontains=q)
        results = []
        for rs in news:
            news_json = {}
            news_json = rs.title
            results.append(news_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            messages.warning(request,'Giriş İşlemi Başarısız. Bilgileri Kontrol Edin.')
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {'category': category,

              }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request,user)
            return HttpResponseRedirect('/')
    form = SignUpForm()
    category = Category.objects.all()
    context ={ 'category' : category,
               'form': form,

    }
    return render(request, 'signup.html', context)