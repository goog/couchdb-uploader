from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from upload.models import UserProfile

class UploadFileForm(forms.Form):
    description = forms.CharField(max_length=100)
    tags = forms.CharField(max_length=50)
    file  = forms.FileField()




#class RegisterForm(UserCreationForm):
class RegisterForm(ModelForm):
    username  = forms.CharField(label=(u'User Name'))
    email     = forms.EmailField(label=(u'Email Address'))
    password1  = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=(u'Verify Password'), widget=forms.PasswordInput(render_value=False))
    birthday = forms.DateField(label=(u'Birthday'))
    name     = forms.CharField(label=(u'Name'))
    favorite = forms.CharField(label=(u'Favorite'))


    class Meta:
        model = UserProfile
        #fields = ("username", "email", )
	exclude = ('user',)

    def clean_email(self):
        email = self.cleaned_data["email"]
 
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
 
        raise forms.ValidationError("A user with that email address already exists.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("That username is already taken, please select another.")

    def clean_password(self):
                if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                        raise forms.ValidationError("The passwords did not match.  Please try again.")
                return self.cleaned_data['password1']




class ProfileForm(ModelForm):
    user  = forms.IntegerField(label=(u'UID'))
    name  = forms.CharField(label=(u'name'))
    birthday  = forms.DateField(label=(u'birthday'))
    favorite  = forms.CharField(label=(u'favorite'))
    class Meta:
        model = UserProfile
	exclude = ('user',)

 
 
    
