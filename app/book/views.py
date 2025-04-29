from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # noqa
from core.models import Book, BookList
from django.core.paginator import Paginator
from book.forms import (
    BookForm,
    BookSearchForm,
)
from django.db.models import Q


def books_view(request):
    form = BookSearchForm(request.GET)
    books_list = Book.objects.all()

    categories = Book.objects.values_list('categories', flat=True)
    unique_categories_list = set()
    for category in categories:
        if category:
            for split in category.split(','):
                unique_categories_list.add(split.strip())

    form.fields['categories'].choices = [
        (cat, cat) for cat in sorted(unique_categories_list)
    ]

    if form.is_valid():
        action = request.GET.get('action')
        query = form.cleaned_data.get('q')

        if action == 'search':
            if query:
                books_list = books_list.filter(
                    Q(title__icontains=query) |
                    Q(authors__icontains=query) |
                    Q(isbn10__icontains=query) |
                    Q(isbn13__icontains=query)
                )

        if action == 'filter' or action == 'search':
            selected_categories = form.cleaned_data.get('categories')
            pages_min = form.cleaned_data.get('pages_min')
            pages_max = form.cleaned_data.get('pages_max')
            rating_min = form.cleaned_data.get('rating_min')
            rating_max = form.cleaned_data.get('rating_max')
            year_min = form.cleaned_data.get('year_min')
            year_max = form.cleaned_data.get('year_max')

            if selected_categories:
                for category in selected_categories:
                    books_list = books_list.filter(categories__icontains=category)

            if pages_min is not None:
                books_list = books_list.filter(num_pages__gte=pages_min)
            if pages_max is not None:
                books_list = books_list.filter(num_pages__lte=pages_max)

            if rating_min is not None:
                books_list = books_list.filter(average_rating__gte=rating_min)
            if rating_max is not None:
                books_list = books_list.filter(average_rating__lte=rating_max)

            if year_min is not None:
                books_list = books_list.filter(published_year__gte=year_min)
            if year_max is not None:
                books_list = books_list.filter(published_year__lte=year_max)

    paginator = Paginator(books_list.order_by('title'), 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'book_list.html', context)


def book_info(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, book_instance=book)
    else:
        form = BookForm(book_instance=book)

    context = {'book': book, 'form': form}
    return render(request, 'book_info.html', context)


def book_add_to_list(request, pk):
    book_to_add = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, book_instance=book_to_add)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.book = book_to_add
            book.save()
            return redirect('books')
    else:
        form = BookForm(book_instance=book_to_add)
    context = {'form': form, 'book': book_to_add}
    return render(request, 'book_add_to_list.html', context)


def book_user_list(request):
    form = BookSearchForm(request.GET)
    books_list = BookList.objects.filter(user=request.user)

    if form.is_valid():
        action = request.GET.get('action')
        if action == 'search':
            query = form.cleaned_data.get('q')
            if query:
                books_list = books_list.filter(
                    Q(book__title__icontains=query) |
                    Q(book__authors__icontains=query) |
                    Q(book__isbn10__icontains=query) |
                    Q(book__isbn13__icontains=query)
                )

        if action == 'filter' or action == 'search':
            selected_statuses = form.cleaned_data.get('statuses')
            if selected_statuses:
                books_list = books_list.filter(status__in=selected_statuses)

        show_favourites = request.GET.get('favourites')
        if show_favourites == 'true' or action == 'favourites':
            books_list = books_list.filter(favourites=True)

    paginator = Paginator(books_list.order_by('book'), 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'form': form}
    return render(request, 'user_list.html', context)


def user_book_info(request, pk):
    book_list_instance = BookList.objects.get(pk=pk)
    book = book_list_instance.book

    form = BookForm(instance=book_list_instance)

    context = {'book': book, 'book_list': book_list_instance, 'form': form}
    return render(request, 'user_book_info.html', context)


def edit_book_view(request, pk):
    book_list = BookList.objects.get(pk=pk, user=request.user)
    book = book_list.book

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'toggle_favourite':
            book_list.favourites = not book_list.favourites
            book_list.save()
            return redirect('user_book_info', pk=pk)

        form = BookForm(request.POST, instance=book_list)

        if action_type == 'change_status':
            if form.is_valid():
                book_list.status = form.cleaned_data['status']
                book_list.save()
                return redirect('user_book_info', pk=pk)

        elif action_type == 'change_pages':
            if form.is_valid():
                book_list.pages_read = form.cleaned_data['pages_read']
                book_list.save()
                return redirect('user_book_info', pk=pk)
    else:
        form = BookForm(instance=book_list)

    context = {
        'form': form,
        'book_list': book_list,
        'book': book,
    }
    return render(request, 'user_book_info.html', context)


def delete_book(request, pk):
    book_instance = BookList.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        book_instance.delete()
        return redirect('user_list')
    return render(request, 'delete_book.html', {'book': book_instance})
