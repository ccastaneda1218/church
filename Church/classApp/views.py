from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


def login_view(request):
    error_message = ''

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            error_message = 'Invalid username or password.'
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
        'error_message': error_message
    }

    return render(request, 'classApp/login.html', context)

def dashboard(request):
    return render(request, 'classApp/dashboard.html')
