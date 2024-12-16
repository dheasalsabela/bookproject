from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from bookproject.books.models import Book, UserProfile, Author, Category, Review

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password2")
#
#         if password != password2:
#             raise forms.ValidationError("Passwords don't match")
#


# class UserloginForm(AuthenticationForm):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

# class UserRegisterForm(UserCreationForm):
#     full_name = forms.CharField(max_length=100, required=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'full_name', 'password1', 'password2']
#
# class LoginForm(AuthenticationForm):
#     username = forms.CharField(max_length=150, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user']

# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['bio']
                  # 'favourite_books']

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
                'class': 'form-control',  # Tambahkan styling jika diperlukan
            }),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write your review...',
                'class': 'form-control',
                'rows': 5,
            }),
        }