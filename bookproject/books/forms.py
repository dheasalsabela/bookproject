from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bookproject.books.models import Book, UserProfile, Author, Category, Review

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'published_date', 'image']

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'image']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control',  # buat menambah styling
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review...',
                'class': 'form-control',
                'rows': 5,
            }),
        }