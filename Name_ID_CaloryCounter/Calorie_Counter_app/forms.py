from django import forms
from Calorie_Counter_app.models import*
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
    class Meta : 
        model = User
        fields = ['username','email','password1','password2']


class LoginForm(AuthenticationForm):
    pass 


class ProfileForm(forms.ModelForm):
    class Meta:
        model = InfoModel
        fields = '__all__'
        exclude = ['bmr','user']
        
class CaloriesForm(forms.ModelForm):
    class Meta:
        model = ConsumedCalModel
        fields = '__all__'
        exclude = ['consumed_by']