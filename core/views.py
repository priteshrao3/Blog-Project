from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.shortcuts import redirect, render, HttpResponseRedirect
from .forms import ContactForm, SignUpForm, LoginForm, PostForm
from django.contrib import messages
from .models import Post

# your home views here.
def home(request):
    post = Post.objects.all()
    return render(request, 'core/home.html', {'posts':post})

def about(request):
    return render(request, 'core/about.html')


 # Simpale Contact Form   
def contact(request):
    fm = ContactForm
    if request.method == 'POST':
        fm = ContactForm(request.POST)
        subject = request.POST['subject']
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        if fm.is_valid():
            messages.success(request, 'Your Messege has been submited successfully')
            fm.save()
            fm = ContactForm()
        else:
            fm = ContactForm()
        send_mail(
            subject,
            name +'\n'+'\n'+ email +'\n'+'\n'+ message,
            settings.EMAIL_HOST_USER,
            ['devloperpritesh@gmail.com'],
            fail_silently=False,
        )
    return render(request, 'core/contact.html', {'form':fm})


# Sign Up Form
def signup(request): 
    form = SignUpForm
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations !! You have Resister Cuccessfully')
            user = form.save()
            group = Group.objects.get(name='Auther')
            user.groups.add(group)
            return HttpResponseRedirect('/login/')
    return render(request, 'core/signup.html', {'form':form})

#Login Form
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = LoginForm(request = request, data = request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username = uname, password = upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            fm = LoginForm()
        return render(request, 'core/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/dashboard/')


# Logout 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Your Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        return render(request, 'core/dashboard.html', {'posts':post})
    else:
        return HttpResponseRedirect('/login/')


# Add Post View
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request, 'core/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


# Update post 
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'core/update.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')



# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


# User Profile
def profile(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = user.get_full_name()
        gps = user .groups.all()
        return render(request, 'core/profile.html', {'full_name': full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/dashboard/')
