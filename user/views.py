from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from news.models import Category,Comment
from user.models import UserProfile
from user.forms import UserUpdateForm,ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from content.models import Menu,Content,ContentForm
from content.models import ContentImageForm,CImages


# Create your views here.

def index(request):
    category = Category.objects.all()
    current_user = request.user #Access user session information
    profile = UserProfile.objects.get(user_id=current_user.id)

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

@login_required(login_url='/login') #Check Login
def addcontent(request):
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save() #veritabanına kayıt
            messages.success(request,'Your Content Insterted Successfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.warning(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'category' : category,
            'menu' : menu,
            'form' : form,
        }
        return render(request,'user_addcontent.html',context)


@login_required(login_url='/login') #Check Login
def contents(request):
    category = Category.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    contents = Content.objects.filter(user_id = current_user.id)
    context = {
        'category' : category,
        'menu' : menu,
        'contents' : contents,
    }
    return render(request, 'user_contents.html',context)

@login_required(login_url='/login') #Check Login
def contentedit(request,id):
    content = Content.objects.get(id=id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Content Updated Successfuly')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.error(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/' + str(id))
    else:
        category = Category.objects.all()
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category' : category,
            'menu' : menu,
            'form' : form,
        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login') #Check Login
def contentdelete(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content Deleted...')
    return HttpResponseRedirect('/user/contents')


def contentaddimage(request,id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your Image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content = Content.objects.get(id=id)
        images = CImages.objects.filter(content_id=id)
        form = ContentImageForm()
        context = {
            'content' : content,
            'images' : images,
            'form' : form,
        }
        return render(request, 'content_gallery.html',context)




