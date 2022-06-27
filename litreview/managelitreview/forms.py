from django import forms
from django.forms import ClearableFileInput, Textarea, ChoiceField
from django.forms.widgets import RadioSelect

from .models import Ticket, Review


RATING_CHOICES = [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")]


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": Textarea(attrs={"cols": "60", "rows": "20"}),
            "image": ClearableFileInput(attrs={"accept": "image/x-png, image/jpeg"}),
        }


class ReviewForm(forms.ModelForm):
    rating = ChoiceField(choices=RATING_CHOICES, widget=RadioSelect())

    class Meta:
        model = Review

        fields = ["rating", "headline", "body"]

        widgets = {
            "body": Textarea(attrs={"cols": "60", "rows": "20"}),
        }
