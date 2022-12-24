from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

def home(request):
    posts=Post.objects.all() 
    return render(request, 'blogapp/home.html',{'posts':posts})#

def about(request):
    return render(request ,'blogapp/about.html')

def contact(request):
    return render(request ,'blogapp/contact.html')

#dasbord will be accese by only authenticated people
#so those user not have logined and try to acces dashboard send them in login page
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        #for getting full name from database we have a built in method full_name
        user = request.user
        full_name = user.get_full_name()
        gps=user.groups.all()
        return render(request ,'blogapp/dashboard.html',{'posts':posts,'full_name':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login.html/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_signup(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congraluations ! You have become an Author, Thanks for be member!")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(request ,'blogapp/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = LoginForm(request=request ,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upassword=form.cleaned_data['password']
                user=authenticate(username=uname,password=upassword)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Loged in success")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LoginForm()
        return render(request,'blogapp/login.html',{'form':form}) 
        return HttpResponseRedirect('/dashboard/')

def add_Post(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                #title->database wala title,title->form se ane wala title
                pst = Post(title=title,desc=desc)
                pst.save()
                form = PostForm() 
        else:
            form = PostForm()
        return render(request,'blogapp/addpost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')

def update_Post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request,'blogapp/update.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')

def delet_Post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login')