from django.db import models
from django.urls import reverse
import uuid

# модель книжных жанров


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Введите жанр книги (документальная, роман и т. д.)")

    # Возврат строки для представления объекта модели
    def __str__(self):
        return self.name

# модель книг (но не конкретных экземпляров)


class Book(models.Model):
    title = models.CharField(
        max_length=200)
    # Используется Foreign Key, потому что у книги может быть только один автор, но у авторов может быть несколько книг
    author = models.ForeignKey(
        'Author',
        on_delete=models.SET_NULL,
        null=True)
    summary = models.TextField(
        max_length=1000,
        help_text="Введите краткое описание книги")
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='тринадцатисимвольный <a href="https://bookscriptor.ru/articles/80712/"> номер ISBN</a>')
    # Используется ManyToManyField, поскольку жанр может содержать много книг. Книги могут охватывать многие жанры
    genre = models.ManyToManyField(
        Genre,
        help_text="Выберите жанр книги\n")

    # Возврат строки для представления объекта модели
    def __str__(self):
        return self.title

    # Создает строку для жанра. Это необходимо для отображения жанра в Admin.
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'
# TODO: почиеить get_absolute_url
    # Возврат URL-адреса для доступа к конкретному экземпляру книги.

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

# модель конкретных экземпляров книг


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Уникальный ID этой книги в библиотеке")
    book = models.ForeignKey(
        'Book',
        on_delete=models.SET_NULL,
        null=True,
        help_text="Наименование книги")
    imprint = models.CharField(
        max_length=200,
        help_text="Штамп")
    due_back = models.DateField(
        null=True,
        blank=True,
        help_text="Дата возврата")
    LOAN_STATUS = (
        ('m', 'Техническое обслуживание'),
        ('o', 'Выдан'),
        ('a', 'Доступен'),
        ('r', 'Зарезервировано'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True, default='m',
        help_text='Статус книги')

    class Meta:
        ordering = ["due_back"]

    # Возврат строки для представления объекта модели
    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)

    fieldsets = (
        (None, {
            'fields': (
                'book',
                'imprint',
                'id')
        }),
        ('Availability', {
            'fields': (
                'status',
                'due_back')
        }),
    )

# модель авторов книг


class Author(models.Model):
    first_name = models.CharField(
        max_length=100,
        help_text='Имя автора')
    last_name = models.CharField(
        max_length=100,
        help_text='Фамилия автора')
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text='Дата рождения')
    date_of_death = models.DateField(
        'Died',
        null=True,
        blank=True,
        help_text='Дата смерти (необязательно)')

    # Возвращает URL-адрес для доступа к конкретному экземпляру автора
    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    # Возврат строки для представления объекта модели
    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
