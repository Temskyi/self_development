from django import forms
from django.db.models import Q

from .models import Dish, Product


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'calories', 'protein',
                  'fat', 'carbohydrates', 'image']

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['dish', 'weight']

    def __init__(self, user_id=Dish.objects.all(), *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        self.fields['dish'].queryset = Dish.objects.filter(Q(creator=user_id) | Q(creator=None))