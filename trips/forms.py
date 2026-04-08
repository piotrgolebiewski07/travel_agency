from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    rating = forms.ChoiceField(
        choices=[
            (5, "5 ⭐"),
            (4, "4 ⭐"),
            (3, "3 ⭐"),
            (2, "2 ⭐"),
            (1, "1 ⭐"),
        ],
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Review
        fields = ["name", "rating", "comment"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "placeholder": "Your review"}),
        }

    def clean_rating(self):
        rating = int(self.cleaned_data.get("rating"))

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")

        return rating
