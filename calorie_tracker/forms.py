from django import forms
from .models import Dish


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'calories', 'protein', 'fat', 'carbohydrates', 'image']

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
