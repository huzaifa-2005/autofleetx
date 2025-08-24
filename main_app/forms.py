from django import forms
from django.contrib.auth.forms import UserCreationForm 

from .models import CustomUser,Car
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

# Case 1: user has no password (Google login)
class CustomSetPasswordForm(SetPasswordForm):
    pass

# Case 2: user has a password
class CustomPasswordChangeForm(PasswordChangeForm):
    pass


class AdminCarForm(forms.ModelForm): # for admin adding car
    class Meta:
        
        model = Car
        fields = ['name', 'brand', 'seating_capacity', 'rent_per_day','model_year','image'
                  ,'vehicle_type','accident_history']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'address')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #  Removing password help texts
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''
    
class CustomUserLoginForm(forms.Form):   # for login_view
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)  

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','address','email','balance']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your address',
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={'placeholder':"Enter Username ", 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder':"Enter First Name", 'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder':"Enter Last Name", 'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'placeholder':"Connect with your authenticated Google account", 'class': 'form-control'}),
        } 
    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        if " " in username:
            raise forms.ValidationError("Usernames cannot contain spaces. Please choose a different one.")
        return username          
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['address'].required = True
        # If the user already has an email, make it read-only in the form
        if self.instance and self.instance.email:
            self.fields['email'].disabled = True    

        self.fields['balance'].disabled = True


class AddBalanceForm(forms.Form):  # for profile_view (when user wants to add balance)
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=None,
        min_value=1,
        help_text='Enter amount to add to your balance'
    ) 