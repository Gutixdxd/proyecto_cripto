from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Document
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fiels = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de Usuario", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Contraseña", max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
    
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error('username', 'Usuario o contraseña incorrectos')
        
        cleaned_data = super().clean()
        return cleaned_data
    
class New_Doc_Form(forms.ModelForm):
   text = forms.CharField(label="Documento", widget=forms.Textarea(attrs={'class': 'form-control', "placeholder": "Escribe tu documento", "cols": "40", "rows": "5"}))
   class Meta:
       model = Document
       fields = ['text']