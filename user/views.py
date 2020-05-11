from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from news.models import Category,Comment
from user.models import UserProfile
from user.forms import UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required



# Create your views here.

def index(request):
    category = Category.objects.all()
    current_user = request.user #Access user session information
    profile = UserProfile.objects.get(pk=current_user.id)

    context ={'category' : category,
              'profile' : profile,
              }
    return render(request, 'user_profile.html',context)

def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request , 'Your account has been updated!')
            return redirect('/user')

    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user) #Important!
            messages.success(request, 'Your password was successfully update!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html', {
            'form' : form,
            'category' : category
        })


@login_required(login_url='/login') #Check Login
def comments(request):
    category = Category.objects.all()
    current_user =request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category' : category,
        'comments' : comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login') #Check Login
def deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id , user_id=current_user.id).delete()
    messages.success(request, 'Comment Deleted...')
    return HttpResponseRedirect('/user/comments')




