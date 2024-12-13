from django.contrib import admin

from bookproject.books.models import UserBookCollection, Book, Author, Category, Review
# from bookproject.books.views import Book, Author, Category, Review
# Register your models here.

# admin.site.register(Book)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # 1. Menampilkan kolom tertentu di daftar admin
    list_display = ('title', 'author', 'category','published_date')

    # 2. Menambahkan pencarian berdasarkan judul dan penulis
    search_fields = ('title', 'author')

    # 3. Menambahkan filter berdasarkan kategori dan status
    list_filter = ('category',)

    # 4. Menentukan urutan default (berdasarkan tanggal publikasi)
    ordering = ('-published_date',)

    # 5. Menjadikan kolom status bisa diubah langsung
    # list_editable = ('status',)

@admin.register(UserBookCollection)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_at', 'status')
    search_fields = ('user', 'book')
    ordering = ('-added_at',)

# Untuk model lain, Anda juga dapat menambahkan kustomisasi serupa:
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'comment')
    search_fields = ('book__title', 'user__user__username')
    list_filter = ('rating',)
