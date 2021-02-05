from django import forms
from django.forms import ModelForm, widgets
from .models import AuctionListing, Comment, Bid

class AuctionListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['product_name', 'price', 'description', 'category', 'image']
        labels = {
            'price': 'Starting Bid',
            'image': 'Image URL (optional)'
        }
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
        }

class CommentForm(ModelForm):
    class Meta: 
        model = Comment
        fields = ['comment']
        labels = {
            'comment': 'Add a comment'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }

class BidForm(ModelForm):
    class Meta: 
        model = Bid
        fields = ['value']
        widgets = {
            'value': forms.NumberInput(attrs={'class': 'form-control'})
        }
        labels = {
            'value': 'Bid value must be greater than current price'
        }