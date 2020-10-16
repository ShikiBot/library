from django.contrib import admin
from .models import Author, Genre, Book, BookInstance

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance) 

class BooksInline(admin.TabularInline):
    model = Book 

# Определите класс администратора
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death') 
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')] 
    inlines = [BooksInline]

# Регистрация класса AuthorAdmin со связанной моделью
admin.site.register(Author, AuthorAdmin) 

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

# Регистрация класса администратора для Book с помощью декоратора
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre') 
    inlines = [BooksInstanceInline]    

# Регистрация класса администратора для BookInstance с помощью декоратора
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    list_display = ('book', 'status', 'due_back', 'id') 

    # код для отображения книги, статуса, даты возврата, и id

