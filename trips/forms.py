from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "placeholder": "Your review"}),
        }

    def clean_rating(self):
        rating = self.cleaned_data.get("rating")

        if rating is None:
            raise forms.ValidationError("Rating is required")

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")

        return rating


class ContactForm(forms.Form):
    your_name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "style": "max-width: 400px;"
        })
    )

    your_email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "style": "max-width: 400px;"
        })
    )

    your_message = forms.CharField(
        label="Message",
        max_length=1000,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "style": "max-width: 800px; max-height: 200px;"
        })
    )

