from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from home.models import Setting, ContactFormu,ContactFormMessage
from news.models import News,Category,Images

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
    setting = Setting.objects.get(pk=1)
    context={"setting" : setting}
    return render(request, 'hakkimizda.html', context)

def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context={"setting" : setting}
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
    context={"setting" : setting,'form' : form}
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
    context = {'new': new,
               'category': category,
               'images': images,
               }
    return render(request,'news_detail.html',context)
