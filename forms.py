from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from users.models import Profile
from Post.models import Comment
from PIL import Image
from django.forms.widgets import DateInput


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Enter your email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'dob', 'bio', 'college', 'year_in_college',]
        widgets = {
            'dob': DateInput(attrs={'type': 'date'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', ]
        widgets = {
            'text': forms.Textarea(attrs={
                'required': True,
                'placeholder': 'Your thoughts...'
            })
        }
