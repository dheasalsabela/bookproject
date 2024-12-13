from django.urls import path
# from django.contrib.auth import views as auth_views
from bookproject.books import views
from bookproject.books.views import BookDetailView

app_name = 'books'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

# PRIVATE
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('add/', views.add_book_to_collection, name='add_book' ),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('author/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.AuthorBookListView.as_view(), name='author_books'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryBookListView.as_view(), name='category_books'),
    path('detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('review/<int:pk>/', views.ReviewCreateView.as_view(), name='review_create'),
    path('update_book_status/<int:pk>/', views.update_book_status, name='update_book_status'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),

# (template_name='public/login.html'),
]