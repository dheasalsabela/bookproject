from django.contrib import admin
from bookproject.books.models import UserBookCollection, Book, Author, Category, Review
# admin.site.register(Book)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # menampilkan kolom tertentu dihalaman admin
    list_display = ('title', 'author', 'category','published_date')

    # menambahkan pencarian berdasarkan judul dan penulis
    search_fields = ('title', 'author__name')

    # menambahkan filter berdasarkan kategori
    list_filter = ('category',)

    # menentukan urutan berdasarkan tanggal publish
    ordering = ('-published_date',)

    # mengubah kolom
    list_editable = ('category',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'author', 'category')
        }),
        ('Additional Details', {
            'fields': ('description', 'published_date'),
            'classes': ('collapse',),  # gunakan fitur collapse untuk menyembunyikan bagian ini secara default
        }),
    )

@admin.register(UserBookCollection)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'added_at', 'status')
    search_fields = ('user__username', 'book__title')
    ordering = ('-added_at',)

    fieldsets = (
        ('Book Collection', {
            'fields': ('user', 'book', 'status')
        }),
        ('Metadata', {
            'fields': ('added_at',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)
    ordering = ('name',)

    fieldsets = (
        ('Author Details', {
            'fields': ('name', 'date_of_birth')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

    fieldsets = (
        ('Category Information', {
            'fields': ('name',)
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'comment')
    search_fields = ('book__title', 'user__username')
    list_filter = ('rating',)

    fieldsets = (
        ('Review Information', {
            'fields': ('book', 'user', 'rating')
        }),
        ('Comment', {
            'fields': ('comment',),
        }),
    )
