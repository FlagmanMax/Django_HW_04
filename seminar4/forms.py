import datetime

from django import forms

from seminar2.models import Product
from seminar3.models import Author, Post


class Form1(forms.Form):
    games = forms.ChoiceField(choices=((1, "heads_tails"), (2, "dices"), (3, "rand")))
    quant = forms.IntegerField(min_value=1, max_value=64,
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))


class Form2(forms.Form):
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'user@mail.ru'}))


class Form3(forms.Form):
    title = forms.CharField(max_length=50,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    author = forms.ModelChoiceField(label='Author', empty_label='Please select', queryset=Author.objects.all(),
                                    widget=forms.Select(attrs={'class': 'form-control'}))


class Form4(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    post = forms.ModelChoiceField(label='Post', empty_label='Please select',
                                  queryset=Post.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}))


class Form5(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class Form6(forms.Form):
    product = forms.ModelChoiceField(label='Product', empty_label='Please select',
                                     queryset=Product.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    img = forms.ImageField()
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    prod_quant = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ImageForm(forms.Form):
    image = forms.ImageField()
