from  django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import *




def home(request):
    
    records = Record.objects.all()

    if request.method == "POST":
        username = request.POST ['username']
        password = request.POST ['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again...")
            return redirect('home')

    return render(request, 'home.html', {'records': records})


def register(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        
        else:
            form = SignUpForm()
            return render(request, 'register.html', {'form': form})

            
    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have beed logged out...")
    return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
             add_record = form.save()
             messages.success(request, "Record Added...")
             return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
         messages.success(request, "You Must Be Logged In...")
         return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully..")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In..")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:     
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Succeesfully...")
        return redirect('home')
    else:
        messages.success(request, "You Must Be Logged In..")
        return redirect('home')
    
