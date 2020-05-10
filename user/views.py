from django.shortcuts import render
from django.http import HttpResponse
from news.models import Category
from user.models import UserProfile



# Create your views here.

def index(request):
    category = Category.objects.all()
    current_user = request.user #Access user session information
    profile = UserProfile.objects.get(pk=current_user.id)

    context ={'category' : category,
              'profile' : profile,
              }
    return render(request, 'user_profile.html',context)