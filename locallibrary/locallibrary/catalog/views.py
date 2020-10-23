from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic

# Функция отображения для домашней страницы сайта.


def index(request):
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    # Метод 'all()' применен по умолчанию.
    num_authors = Author.objects.count()
    num_genre_with_word = Genre.objects.filter(
        name__contains='Научная').count()
    num_books_with_word = Book.objects.filter(
        title__contains='Надежность').count()

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={
            'num_books': num_books,
            'num_instances': num_instances,
            'num_instances_available': num_instances_available,
            'num_authors': num_authors,
            'num_genre_with_word': num_genre_with_word,
            'num_books_with_word': num_books_with_word,
        },
    )


class BookListView(generic.ListView):
    model = Book

    def get_queryset(self):
        # Получить 5 книг, содержащих 'war' в заголовке
        # return Book.objects.filter(title__contains='war')[:5]
        return Book.objects.all()
