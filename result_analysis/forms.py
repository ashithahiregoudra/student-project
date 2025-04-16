# forms.py
from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        

from .models import Review

#class ReviewForm(forms.ModelForm):
    #class Meta:
     #   model = Review
      #  fields = ['rating', 'comment']
       # widgets = {
        #    'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),  # Rating from 1 to 5
         #   'comment': forms.Textarea(attrs={'rows': 4}),
        #}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']  # Include the fields you want to capture




# result_analysis/forms.py
from django import forms

class SubjectForm(forms.Form):
    name = forms.CharField(label='Subject Name', max_length=100)
    difficulty = forms.ChoiceField(label='Difficulty Level', choices=[(i, str(i)) for i in range(1, 6)])
    time_required = forms.IntegerField(label='Time Required (hours)', min_value=1, max_value=7)
    importance = forms.ChoiceField(label='Importance Level', choices=[(i, str(i)) for i in range(1, 6)])


from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Your feedback here...', 'rows': 4}),
        }
