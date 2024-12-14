from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from bookproject.books.forms import BookForm, UserProfileForm, ReviewForm
# from bookproject import books
from bookproject.books.forms import BookForm, UserRegisterForm
from bookproject.books.models import Book, Author, Category, Review, UserProfile, UserBookCollection


# Create your views here.

# PUBLIC PART
def index(request):
    return render(request, 'public/index.html')

def about(request):
    return render(request, 'public/about.html')

def register_view(request):
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Account was created.')
                return redirect('books:login')
        else:
            form = UserRegisterForm()
        return render(request, 'public/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Selamat datang')
                return redirect('books:dashboard')
            else:
                messages.error(request, 'Username atau password salah.')
        else:
            messages.error(request, 'Formulir tidak valid. Silakan periksa kembali.')
    else:
        form = AuthenticationForm()

    return render(request, 'public/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('books:login')

@login_required
def dashboard(request):
    # if request.method == 'POST' :
    #     for key, value in request.POST.items():
    #         if key.startswith("status_"):
    #             try:
    #                 book_id = int(key.split("_")[1])
    #                 book = UserBookCollection.objects.get(id=book_id, user=request.user)
    #                 if value in ['Reading', 'Completed', 'Wishlist']:
    #                     book.status = value
    #                     book.save()
    #             except (UserBookCollection.DoesNotExist, ValueError):
    #                 continue
    #     return redirect('books:dashboard')

    user_books = UserBookCollection.objects.filter(user=request.user)
    books = Book.objects.all()

    return render(request, 'common/dashboard.html', {
        'user_books': user_books,
        'books': books,
        # 'wishlist_books': wishlist_books,
    })

@login_required
def profile(request):
    completed_books = UserBookCollection.objects.filter(user=request.user, status='Completed')
    # if request.method == 'POST':
    #     form = UserProfileForm(request.POST, request.FILES, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('profile')
    return render(request, 'common/profile.html', {
        'completed_books': completed_books,
    })

@login_required
def edit_profile(request):
    user = request.user

    # Jika form disubmit
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            # Simpan perubahan profil
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('books:profile')  # Redirect ke halaman profil setelah berhasil mengedit
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Jika GET request, tampilkan data pengguna di form
        form = UserProfileForm(instance=user)

    return render(request, 'profiles/edit_profile.html', {'form': form})

#     try:
#         profile = request.user.UserProfile
#     except UserProfile.DoesNotExist:
#         profile = UserProfile(user=request.user)
#         profile.save()
#
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('books:profile')
#     else:
#         form = EditProfileForm(instance=profile)
#
#     return render(request, 'userprofile/edit_profile.html', {'form': form})
# #
@login_required
def add_book_to_collection(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = Book.objects.get(id=book_id)

        # Check if the book is already in the user's collection
        if not UserBookCollection.objects.filter(user=request.user, book=book).exists():
            UserBookCollection.objects.create(user=request.user, book=book)
            return redirect('books:dashboard')  # Redirect to the user's collection page
        else:
            message = "This book is already in your collection."
            return render(request, 'books/add_book.html', {'books': Book.objects.all(), 'message': message})

    # GET request: show all available books
    books = Book.objects.all()
    return render(request, 'books/add_book.html', {'books': books})


@staff_member_required  # Memastikan hanya admin yang bisa mengakses halaman ini
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Setelah menambah buku, alihkan ke daftar buku
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

@login_required
def update_book_status(request, pk):
    user_book = get_object_or_404(UserBookCollection, id=pk, user=request.user)

    if request.method == 'POST':
        # Get the new status from the form
        status_key = f"status_{user_book.book.id}"
        new_status = request.POST.get(status_key)
        if new_status:
            user_book.status = new_status
            user_book.save()

        # Redirect back to the dashboard or wherever needed
        return redirect('books:dashboard')

    return render(request, 'common/dashboard.html', {'user_book': user_book})

# def add_book(request):
#     if request.method == 'GET':
#         form = BookForm
#     else:
#         form = BookForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'books/add_book.html', context)
#
# def edit_book(request, book_id):
#     book = Book.objects.filter(pk=book_id).get()
#
#     if request.method == 'GET':
#         form = BookForm(instance=book)
#     else:
#         form = BookForm(request.POST, instance=book)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     context = {
#         'form': form,
#         'book': book,
#     }
#
#     return render(request, 'books/edit_book.html', context)
#
def delete_book(request, pk):
    try:
        userbook = UserBookCollection.objects.get(pk=pk)
        # Menghapus buku dari koleksi pengguna
        userbook.delete()
        # Redirect ke halaman dashboard setelah menghapus buku
        return redirect('books:dashboard') # Ganti 'dashboard' dengan nama URL dashboard Anda

    except UserBookCollection.DoesNotExist:
        # Jika buku tidak ditemukan
        return redirect('books:dashboard')

    # book = Book.objects.filter(pk=book_id).get()
    #
    # if request.method == 'GET':
    #     form = BookForm(instance=book)
    # else:
    #     form = BookForm(request.POST, instance=book)
    #     if form.is_valid():
    #         book.delete()
    #         return redirect('dashboard')
    # context = {
    #     'form': form,
    #     'book': book,
    # }
    # return render(request, 'books/delete_book.html', context)


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'list/book_list.html'
    context_object_name = 'books'
    # paginate_by = 10 #nampilin 10 buku
#

class BookDetailView(LoginRequiredMixin ,DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ambil buku berdasarkan pk
        book = self.get_object()

        # Ambil semua review untuk buku ini
        reviews = Review.objects.filter(book=book).order_by('-created_at')

        # Tambahkan form dan reviews ke context
        context['reviews'] = reviews
        context['form'] = ReviewForm()  # Form untuk menambah review

        return context

class AuthorListView(LoginRequiredMixin, ListView):
    model = Author
    template_name = 'list/author_list.html'
    context_object_name = 'authors'

class AuthorBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/author_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        author_id = self.kwargs.get('pk')
        return Book.objects.filter(author_id=author_id)

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'list/category_list.html'
    context_object_name = 'categories'

class CategoryBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/category_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        category_id = self.kwargs.get('pk')
        return Book.objects.filter(category_id=category_id)
#
class ReviewCreateView(CreateView):
    model = Review
    template_name = 'reviews/review_create.html'
    form_class = ReviewForm
    # success_url = reverse_lazy('books:book_detail')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        # Menetapkan pengguna yang saat ini sedang login
        form.instance.user = self.request.user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        # Menyimpan review
        return super().form_valid(form)

    def get_success_url(self):
        # Setelah berhasil menambah review, arahkan ke halaman buku
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})

# class ReviewListView(LoginRequiredMixin, ListView):
#     model = Review
#     template_name = 'books/book_detail.html'
#     context_object_name = 'reviews'
#
#     def get_queryset(self):
#         book = get_object_or_404(Book, pk=self.kwargs['book_id'])
#         return Review.objects.filter(book=book).order_by('-created_at')


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
    #     return context
    #
    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
    #     return super().form_valid(form)
    #
    # def get_success_url(self):
    #     return reverse_lazy('books:book_detail', kwargs={'pk': self.kwargs['pk']})


# def register_view(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.profile.full_name = form.cleaned_data.get('full_name')
#             user.save()
#             login(request, user)
#             return redirect('books:login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'public/register.html', {'form': form})
#
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('dashboard')
#     else:
#         form = LoginForm()
#     return render(request, 'public/login.html', {'form': form})

# def book_detail(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     return render(request, 'public/book_detail.html', {'book': book})