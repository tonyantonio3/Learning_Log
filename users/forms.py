from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import re

class CustomCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label = 'Senha',
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )
    password2 = forms.CharField(
        label ='Confirme sua senha',
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua senha'})
    )

    class Meta:
        model = User
        fields = {'username', 'email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
        }
        labels = {
            'username': 'Nome de usuário',
            'email': 'Email',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 4:
            raise forms.ValidationError("O nome de usuário deve ter pelo menos 4 caracteres.")

        if not re.match(r'^[A-Za-z0-9_]+$', username):
            raise forms.ValidationError("O nome de usuário só pode conter letras, números e underline (_).")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está em uso.")



        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("As senhas não coincidem.")
        if len(p1) < 8:
            raise forms.ValidationError("A senha deve conter no mínimo 8 caracteres.")


        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])  #criptografando a senha.
        if commit:
            user.save()
        return user
