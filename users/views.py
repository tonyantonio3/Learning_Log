from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomCreationForm

def logout_view(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('index')

    if request.method != 'POST':
        form = CustomCreationForm()

    else:
        form = CustomCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                request,
                username = new_user.username,
                password = request.POST['password1']
            )
            login(request, authenticated_user)
            messages.success(request, 'Cadastro realizado com sucesso! Você está logado.')
            return redirect('index')

        else:
            messages.error(request, 'Erro no cadastro. Verifique os dados e tente novamente.')

    context = {'form': form}
    return render(request, 'users/register.html', context)

