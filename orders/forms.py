from django import forms
from .models import Order, Review


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name',
            'product_name',
            'quantity',
        ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5
            }),
            'review': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your review here...'
            }),
        }