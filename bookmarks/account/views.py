from django.shortcuts import render,redirect
# from django.http import HttpResponse
from .forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

# def user_login(request):
    
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request,user)
#                     return HttpResponse('Authenticated Successfully')
#                 else:
#                     return HttpResponse('Disabled Account')
#             else:
#                 return HttpResponse('Invalid Login')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html',{'form':form})
    
@login_required  
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.user.is_authenticated:
        messages.error(request,'You are already logged in')
        return redirect('dashboard')
        
    else:
        if request.method == 'POST':
            user_form = UserRegistrationForm(request.POST)
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password1'])
                new_user.save()
                Profile.objects.create(user=new_user)
                
                #log in user
                #user= authenticate(username=new_user , password=user_form.cleaned_data['password1'])
                #login(request, user)
                return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request,'You have been logged out..Thanks see you soon')
    return redirect('login')

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile updated successfully')
        else:
            messages.error(request,'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})