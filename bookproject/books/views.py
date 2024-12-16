from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from bookproject.books.forms import ReviewForm, UserRegisterForm
from bookproject.books.models import Book, Author, Category, Review, UserBookCollection


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
                messages.success(request, 'Account was created. Please Log in')
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
                return redirect('books:dashboard')
            else:
                messages.error(request, 'Incorrect username or password.')
        else:
            messages.error(request, 'The form is invalid. Please check again.')
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
    user_books = UserBookCollection.objects.filter(user=request.user)
    books = Book.objects.all()

    return render(request, 'common/dashboard.html', {
        'user_books': user_books,
        'books': books,
    })

@login_required
def profile(request):
    completed_books = UserBookCollection.objects.filter(user=request.user, status='Completed')

    return render(request, 'common/profile.html', {
        'completed_books': completed_books,
    })

@login_required
def add_book_to_collection_from_quicklinks(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = Book.objects.get(id=book_id)

        # mengecek apakah buku sudah ada di koleksi buku user
        if not UserBookCollection.objects.filter(user=request.user, book=book).exists():
            UserBookCollection.objects.create(user=request.user, book=book)
            return redirect('books:dashboard')
        else:
            message = "This book is already in your collection."
            return render(request, 'books/add_book.html', {'books': Book.objects.all(), 'message': message})

    books = Book.objects.all()
    return render(request, 'books/add_book.html', {'books': books})

@login_required
def add_book_to_collection_from_list(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')

        try:
            # mengambil buku berdasarkan id
            book = Book.objects.get(id=book_id)

            if not UserBookCollection.objects.filter(user=request.user, book=book).exists():
                UserBookCollection.objects.create(user=request.user, book=book)
                return redirect('books:dashboard')
            else:
                messages.warning(request, "This book is already in your collection.")
                return redirect('books:add_booklist')

        except Book.DoesNotExist:
            messages.error(request, "This book was not found.")
            return redirect('books:add_booklist')

    books = Book.objects.all()
    return render(request, 'list/book_list.html', {'books': books})

@login_required
def update_book_status(request, pk):
    user_book = get_object_or_404(UserBookCollection, id=pk, user=request.user)

    if request.method == 'POST':
        # dapatkan status baru dari form
        status_key = f"status_{user_book.book.id}"
        new_status = request.POST.get(status_key)
        if new_status:
            user_book.status = new_status
            user_book.save()

        return redirect('books:dashboard')

    return render(request, 'common/dashboard.html', {'user_book': user_book})

@login_required
def delete_book(request, pk):
    try:
        userbook = UserBookCollection.objects.get(pk=pk)
        userbook.delete()
        return redirect('books:dashboard')

    except UserBookCollection.DoesNotExist:
        return redirect('books:dashboard')

class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'list/book_list.html'
    context_object_name = 'books'

class BookDetailView(LoginRequiredMixin ,DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # mengambil buku berdasarkan pk
        book = self.get_object()

        # mengambil semua review
        reviews = Review.objects.filter(book=book).order_by('-created_at')

        # menambah form dan review ke context
        context['reviews'] = reviews
        context['form'] = ReviewForm()  # form untuk menambah review

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
        author_id = self.kwargs['pk']  # ambil id dari url
        self.author = get_object_or_404(Author, pk=author_id)  # ambil penulis yg dipilih yg sesuai dengan idnya
        return Book.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author  # menambah penulis ke context
        return context

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'list/category_list.html'
    context_object_name = 'categories'

class CategoryBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/category_books.html'
    context_object_name = 'books'

    def get_queryset(self):
        category_id = self.kwargs['pk']
        self.category = get_object_or_404(Category, pk=category_id)
        return Book.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'reviews/review_create.html'
    form_class = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        # menetapkan user yang saat ini login
        form.instance.user = self.request.user
        form.instance.book = get_object_or_404(Book, pk=self.kwargs.get('pk'))
        # menyimpan review
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.book.pk})
