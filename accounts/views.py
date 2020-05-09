from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User


def user_login(request):
    register_form = RegistrationForm
    form = LoginForm
    if request.method == 'POST':
        if request.POST.get('submit') == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        user_id = User.objects.get(username=user)
                        return redirect('/accounts/profile/'+str(user_id.id))
                    else:
                        return HttpResponse('Disabled account')
                else:
                    return HttpResponse('Invalid login')
        elif request.POST.get('submit') == 'Create':
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                print(register_form.cleaned_data)
                new_user = register_form.save(commit=False)
                new_user.set_password(register_form.cleaned_data['password'])
                new_user.save()
                cd = register_form.cleaned_data
                username = cd['username']
                user_id = User.objects.get(username=username)
                return redirect('/accounts/profile/'+str(user_id.id))
            else:
                print('invalid')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form, 'register_form': register_form})


@login_required
def profile(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'accounts/profile.html', {'user': user})
