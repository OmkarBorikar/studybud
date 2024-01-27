from django.forms import ModelForm

from .models import Room

class RoomForm(ModelForm):
    class Meta:         # class used for setting up the meta data
        model = Room    # record we want to use on form
        fields = '__all__' # we can specify list of fields we want to display on form 