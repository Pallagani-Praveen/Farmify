from django import forms
from django.forms import fields
from django.forms.fields import ChoiceField
from auths.models import User

class UserCreationFrom(forms.Form):
    email = forms.EmailField(label='Email',max_length=50,required=True)
    first_name = forms.CharField(label='First Name',max_length=50,required=False)
    second_name = forms.CharField(label='Second Name',max_length=50,required=False)
    password = forms.CharField(label='Password',widget=forms.PasswordInput,max_length=50,required=True)
    avatar = forms.ImageField(label='Choose Avatar ',required=False)
    CHOICES = [('farmer','Farmer'),('dealer','Dealer')]
    GENDERS = [('male','MALE'),('female','FEMALE')]
    gender = forms.ChoiceField(choices=GENDERS,widget=forms.RadioSelect,required=True)
    role = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect,required=True)


    def clean(self):
        super(UserCreationFrom,self).clean()
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        

        index = email.index('@')
        if email[index:] != '@gmail.com':
            self._errors['email'] = self.error_class(['Use Gmail Account Only'])

       
        first_name = self.cleaned_data.get('first_name')
        if len(first_name)!=0 and len(first_name)<4:
            self._errors['first_name'] = self.error_class(['Length should be alteast 4 charecters'])

       
        second_name = self.cleaned_data.get('second_name')
        if len(second_name)!=0 and len(second_name)<4:
            self._errors['second_name'] = self.error_class(['Length should be alteast 4 charecters'])

        if len(password)<8 or not password.isalnum():
            self._errors['password'] = self.error_class(['Length should be alteast 8 alpha numeric charecters'])

        return self.cleaned_data

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email',max_length=50)
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    CHOICES = [('farmer','Farmer'),('dealer','Dealer')]
    role = forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
    