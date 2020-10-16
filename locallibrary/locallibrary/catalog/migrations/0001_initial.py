# Generated by Django 3.1.2 on 2020-10-16 06:16

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(help_text='Имя автора', max_length=100)),
                ('last_name', models.CharField(help_text='Фамилия автора', max_length=100)),
                ('date_of_birth', models.DateField(blank=True, help_text='Дата рождения', null=True)),
                ('date_of_death', models.DateField(blank=True, help_text='Дата смерти (необязательно)', null=True, verbose_name='Died')),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(help_text='Введите краткое описание книги', max_length=1000)),
                ('isbn', models.CharField(help_text='тринадцатисимвольный <a href="https://bookscriptor.ru/articles/80712/"> номер ISBN</a>', max_length=13, verbose_name='ISBN')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.author')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите жанр книги (документальная, роман и т. д.)', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Уникальный ID этой книги в библиотеке', primary_key=True, serialize=False)),
                ('imprint', models.CharField(help_text='Штамп', max_length=200)),
                ('due_back', models.DateField(blank=True, help_text='Дата возврата', null=True)),
                ('status', models.CharField(blank=True, choices=[('m', 'Техническое обслуживание'), ('o', 'Выдан'), ('a', 'Доступен'), ('r', 'Зарезервировано')], default='m', help_text='Статус книги', max_length=1)),
                ('book', models.ForeignKey(help_text='Наименование книги', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.book')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(help_text='Выберите жанр книги\n', to='catalog.Genre'),
        ),
    ]
