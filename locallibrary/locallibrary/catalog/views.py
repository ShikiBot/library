from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from .forms import RenewBookForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author

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

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooks(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':datetime.date.today,}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')