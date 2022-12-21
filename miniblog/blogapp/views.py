from django.shortcuts import render,HttpResponseRedirect
#by default django ki traf se milne wala signup form use kar rhe hai yah
#skip this by default form,from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

def home(request):
    posts=Post.objects.all() #post model se sre post nikalo and creates posts key and render it to templates
    return render(request, 'blogapp/home.html',{'posts':posts})#

def about(request):
    return render(request ,'blogapp/about.html')

def contact(request):
    return render(request ,'blogapp/contact.html')

#dasbord ko kewal authenticated yani login kiya hua hi person acces kar sakta 
#so jo login ni send them to login page if they try to open dashboard
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
        #if request kiya gya post mehod then store post data in form and validate it the given data id valid or not
        form=SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request,"Congraluations ! You have become an Author, Thanks for be member!")
            user = form.save()
            # jo v new banda sighnup karega ham use author group assign kar de rhe hai
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()   #use this form in signup.html
    return render(request ,'blogapp/signup.html',{'form':form})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            form = LoginForm(request=request ,data=request.POST)
            if form.is_valid():
                #cleaned.data me wahi name dalna jo username and password ko diya u can check it by inspecting chrome
                uname=form.cleaned_data['username']
                upassword=form.cleaned_data['password']
                user=authenticate(username=uname,password=upassword)
                if user is not None:
                    login(request,user)
                    messages.success(request,"Loged in success")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LoginForm()
        return render(request,'blogapp/login.html',{'form':form}) #{'form':form} yaha ek form name ka key ham vehj rhe hai login.html me
    else:
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
                form = PostForm() #blank kar diye us form ko        return render(request,'blogapp/addpost.html')
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
        #ye post method isliye aa rha q ki delet ko hmne form ke form me rakha hai check karo dashboard.html kos
        #delete pe jab click karenge dashboard.html se post method ayega
        if request.method=="POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login')