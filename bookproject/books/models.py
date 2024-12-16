from django.db import models
from django.contrib.auth.models import User
# from django.conf import settings
# from django.utils import timezone


# class Customuser(AbstractUser):
#     bio = models.TextField(max_length=500, blank=True)
# 
#     def __str__(self):
#         return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one to one dg user

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    image = models.URLField()
    # ImageField(upload_to='images/author/', null=True, blank=True))

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #one to many dgn cat
    published_date = models.DateField()
    image = models.URLField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # one to many dgn user

    def __str__(self):
        return self.title

class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    book = models.ForeignKey(Book, on_delete=models.CASCADE) #one to many dg book
    user = models.ForeignKey(User, on_delete=models.CASCADE) #one to many dgn user
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.book.title}"

class UserBookCollection(models.Model):
    STATUS_CHOICES = [
        ('Reading', 'Reading'),
        ('Completed', 'Completed'),
        ('Wishlist', 'Wishlist'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Wishlist')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# class Recommendation(models.Model):
#     name = models.CharField(max_length=50)
#     books = models.ManyToManyField(Book)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name