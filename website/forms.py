from django import forms
from website.models import *
from django.contrib.auth import login, logout, authenticate
from django.core.validators import MinLengthValidator, MinValueValidator, \
RegexValidator, URLValidator
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets  


duration = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
)

class SlotsForm(forms.ModelForm):
    dates = forms.DateField(widget=forms.widgets.SelectDateWidget)
    class Meta:
        model = Slot
        fields = [
            "dates",
            ]

class WorkshopForm(forms.ModelForm):
	title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
                        required = True,
                        label = "Title",
                        error_messages = {'required':'Title field required.'},  
                        )
	about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Me'}),
                        required = True,
                        label = "About",
                        error_messages = {'required':'About me field required.'},  
                        )
	instruct_part = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Instructions for Participant'}),
                        required = True,
                        label = "Instructions fot Participants",
                        error_messages = {'required':'Instructions for Participants field required.'},  
                        )
	instruct_coord = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Instructions for Co-ordinator'}),
                        required = True,
                        label = "Instructions for Co-ordinator",
                        error_messages = {'required':'Instructions for Co-ordinator field required.'},  
                        )
	duration = forms.ChoiceField(choices=duration, label = 'Duration (days.)')

	schedule = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                        label = 'Please upload Workshop schedule',
                        required = False,)  

	tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
                        required = False,
                        label = "Tags"
                        )
    
	class Meta:
		model = Workshop
		fields = [
			"title",
			"about",
			"instruct_part",
			"instruct_coord",
			"duration",
			"schedule",
			"tag"
		]
        # dates = forms.DateField(widget=forms.widgets.SelectDateWidget)

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'username', 'password1',
		          'password2')
        first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
                        label = 'First Name'
                        )
        last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
                        label = 'Last Name'
                        )
        email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}),
                        required = True,
                        error_messages = {'required':'Email field required.'},  
                        label = 'Email'
                        )
        username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                        required = True,
                        error_messages = {'required':'Username field required.'},  
                        label = 'Username'
                        )
        password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                        required = True,
                        error_messages = {'required':'Password field required.'},  
                        label = 'Password'
                        )
        password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
                        required = True,
                        error_messages = {'required':'Password Confirm field required.'},  
                        label = 'Re-enter Password'
                        )
    
        def clean_first_name(self):
            return self.cleaned_data["first_name"].title()

        def clean_email(self):
            return self.cleaned_data["email"].lower()

        def clean_last_name(self):
            return self.cleaned_data["last_name"].title()


class UserLoginForm(forms.Form):
    username = forms.CharField(
			widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), 
			label=''
		)
    password = forms.CharField(
			widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), 
			label=''
		)

class BookslotForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address'}),
                        required = True,
                        error_messages = {'required':'Address field required.'},  
                        )
    participants = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'No. of Participants'}),
                        required = True,
                        label = 'No. of Participants'
                        )
    class Meta:
        model = Booking
        fields = [
            "address",
            "participants"
            ]