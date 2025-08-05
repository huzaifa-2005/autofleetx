from django import forms
from django.contrib.auth.forms import UserCreationForm 

from .models import CustomUser,Car

'''UserCreationForm--its a prebuilt Django form 
to create a new user safely, with built-in password confirmation handling.'''

''' The Meta class inside our class based forms tells Django how to build the form from the model by providing 
        configuration like which model and fields to use. '''

class AdminCarForm(forms.ModelForm): # for admin_add_car view
    class Meta:
        
        model = Car
        fields = ['name', 'brand', 'seating_capacity', 'rent_per_day','model_year','image'
                  ,'vehicle_type','accident_history']
        # fields defines the model's fields to be included in the form.
        # exclude defines the model's fields to be excluded from the form.



class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #  Remove password help texts
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
class CustomUserLoginForm(forms.Form):   # for login_view
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)  # to make password field hidden



class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['address']
        widgets = {
            'address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Enter your address',
                'class': 'form-control'
            }),
        }


class AddBalanceForm(forms.Form):  # for profile_view (when user wants to add balance)
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=None,
        min_value=1,
        help_text='Enter amount to add to your balance'
    )