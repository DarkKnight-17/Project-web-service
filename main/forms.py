from .models import Services, Auto_parts, Car
from django.forms import ModelForm ,TextInput, IntegerField

class Carform(ModelForm):
    class Meta:
        model = Car
        fields = '__all__'
        exclude = ['user']