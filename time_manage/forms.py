from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.forms import ModelForm, DateInput
from time_manage.models import Event
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ( 'title', 'category','start_time', 'end_time')

  def __init__(self, *args, **kwargs):
    print ('come here in forms')
    print (kwargs)
    # user = kwargs.pop('object_list')
    # user = kwargs.pop('event_list')
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    # self.fields['object_list'].queryset = Event.objects.filter(user=user)
    # self.fields['event_list'].queryset = Event.objects.filter(user=user)





class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20)
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

class RegistrationForm(forms.Form):
    # first_name = forms.CharField(max_length=20)
    # last_name  = forms.CharField(max_length=20)
    # email      = forms.CharField(max_length=50,
    #                              widget = forms.EmailInput())
    # username   = forms.CharField(max_length = 20)
    # password1  = forms.CharField(max_length = 200, 
    #                              label='Password', 
    #                              widget = forms.PasswordInput())
    # password2  = forms.CharField(max_length = 200, 
    #                              label='Confirm password',  
    #                              widget = forms.PasswordInput())
    
    username   = forms.CharField(max_length = 20)
    password  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput())
    confirm_password  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput())
    # email      = forms.CharField(max_length=50,
    #                              widget = forms.EmailInput())
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)



    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class CreateForm(forms.Form):
    last_name     = forms.CharField(max_length=20)
    first_name    = forms.CharField(max_length=20)
    birthday      = forms.DateField(required=False)
    address       = forms.CharField(required=False, max_length=200)
    city          = forms.CharField(required=False, max_length=30)
    state         = forms.CharField(required=False, max_length=20)
    zip_code      = forms.CharField(required=False, max_length=10)
    country       = forms.CharField(required=False, max_length=30)
    email         = forms.CharField(required=False, max_length=32)
    home_phone    = forms.CharField(required=False, max_length=16)
    cell_phone    = forms.CharField(required=False, max_length=16)
    fax           = forms.CharField(required=False, max_length=16)
    spouse_last   = forms.CharField(required=False, max_length=16)
    spouse_first  = forms.CharField(required=False, max_length=16)
    spouse_birth  = forms.DateField(required=False)
    spouse_cell   = forms.CharField(required=False, max_length=16)
    spouse_email  = forms.CharField(required=False, max_length=32)


class EditForm(forms.Form):
    last_name     = forms.CharField(max_length=20)
    first_name    = forms.CharField(max_length=20)
    birthday      = forms.DateField(required=False)
    address       = forms.CharField(required=False, max_length=200)
    city          = forms.CharField(required=False, max_length=30)
    state         = forms.CharField(required=False, max_length=20)
    zip_code      = forms.CharField(required=False, max_length=10)
    country       = forms.CharField(required=False, max_length=30)
    email         = forms.CharField(required=False, max_length=32)
    home_phone    = forms.CharField(required=False, max_length=16)
    cell_phone    = forms.CharField(required=False, max_length=16)
    fax           = forms.CharField(required=False, max_length=16)
    spouse_last   = forms.CharField(required=False, max_length=16)
    spouse_first  = forms.CharField(required=False, max_length=16)
    spouse_birth  = forms.DateField(required=False)
    spouse_cell   = forms.CharField(required=False, max_length=16)
    spouse_email  = forms.CharField(required=False, max_length=32)

