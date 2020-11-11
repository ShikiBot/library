from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

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
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits+1

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
            'num_visits':num_visits
        },
    )


class BookListView(generic.ListView):
    model = Book
    # ваше собственное имя переменной контекста в шаблоне
    context_object_name = 'my_object_list'
    # Получение 5 книг, содержащих слово 'war' в заголовке
    queryset = Book.objects.filter(title__icontains='war')[:5]
    # Определение имени вашего шаблона и его расположения
    template_name = 'books/my_arbitrary_template_name_list.html'
    paginate_by = 3

    def get_queryset(self):
        # Получить 5 книг, содержащих 'war' в заголовке
        #! return Book.objects.filter(title__icontains='war')[:5]
        return Book.objects.all()

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и иниуиализируем ее некоторым значением
        context['some_data'] = 'Это всего лишь некоторые данные'
        return context


class BookDetailView(generic.DetailView):
    model = Book    

    def book_detail_view(self, request,pk):
        try:
            author_id=Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Книги не существует")
        
        return render(
            request,
            'catalog/book_detail.html',
            context={'book':author_id,}
        )

class AuthorsListView(generic.ListView):
    model = Author
    # ваше собственное имя переменной контекста в шаблоне
    context_object_name = 'my_author_list'
    # Определение имени вашего шаблона и его расположения
    template_name = 'authors/my_arbitrary_template_name_list.html'
    paginate_by = 3 

    def get_queryset(self):
        print(Author.objects.all())
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(AuthorsListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и иниуиализируем ее некоторым значением
        context['some_data'] = 'Это всего лишь некоторые данные'
        return context

class AuthorsDetailView(generic.DetailView):
    model = Author    

    def author_detail_view(self, request,pk):
        try:
            author_id=Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Книги не существует")
        
        return render(
            request,
            'catalog/author_detail.html',
            context={'author':author_id,}
        )

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')