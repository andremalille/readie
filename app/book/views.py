import re

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from core.models import Book, BookList
from django.core.paginator import Paginator
from book.forms import (
    BookForm,
    BookSearchForm,
)
from django.db.models import Q
from django.http import JsonResponse


@login_required()
def books_view(request):
    form = BookSearchForm(request.GET)
    books_list = Book.objects.all()
    sort = False

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
                query = Q()
                for category in selected_categories:
                    query |= Q(categories__icontains=category)
                books_list = books_list.filter(query)

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

        if action == 'recommend':
            sort = True

            user_added_books = Book.objects.filter(booklist__user=request.user)
            books_list = books_list.exclude(pk__in=user_added_books)

            user_favorites = BookList.objects.filter(user=request.user, favourites=True)

            if user_favorites.exists():
                favorite_books = Book.objects.filter(booklist__in=user_favorites)
                user_categories = favorite_books.values_list('categories', flat=True)

                user_unique_categories_list = set()
                for category in user_categories:
                    if category:
                        for split in category.split(','):
                            user_unique_categories_list.add(split.strip())

                if user_unique_categories_list:
                    category_query = Q()
                    for category in user_unique_categories_list:
                        pattern = r'(^|,\s*)' + re.escape(category) + r'(\s*,|$)'
                        category_query |= Q(categories__regex=pattern)

                    books_list = books_list.filter(category_query)

    if sort:
        books_list = books_list.order_by('-average_rating')
    else:
        books_list = books_list.order_by('title')

    paginator = Paginator(books_list, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']

    context = {
        'page_obj': page_obj,
        'form': form,
        'query_params': query_params.urlencode()
    }
    return render(request, 'book_list.html', context)


@login_required()
def book_info(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, book_instance=book)
    else:
        form = BookForm(book_instance=book)

    context = {'book': book, 'form': form}
    return render(request, 'book_info.html', context)


@login_required()
def book_add_to_list(request, pk):
    book_to_add = get_object_or_404(Book, pk=pk)
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
    return render(request, 'book_info.html', context)


@login_required()
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


@login_required()
def user_book_info(request, pk):
    book_list_instance = get_object_or_404(BookList, pk=pk, user=request.user)
    book = book_list_instance.book

    form = BookForm(instance=book_list_instance)

    context = {'book': book, 'book_list': book_list_instance, 'form': form}
    return render(request, 'user_book_info.html', context)


@login_required()
def edit_book_view(request, pk):
    book_list = get_object_or_404(BookList, pk=pk, user=request.user)
    book = book_list.book
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if request.method == 'POST':
        action_type = request.POST.get('action_type')

        if action_type == 'toggle_favourite':
            book_list.favourites = not book_list.favourites
            book_list.save()
            return redirect('user_book_info', pk=pk)

        if action_type == 'change_status':
            status = request.POST.get('status')
            if status:
                book_list.status = status
                book_list.save()

                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'status_display': book_list.get_status_display()
                    })
                return redirect('user_book_info', pk=pk)
            elif is_ajax:
                return JsonResponse({
                    'success': False,
                    'errors': {'status': 'Status field is required'}
                })

        elif action_type == 'change_pages':
            try:
                pages_read = int(request.POST.get('pages_read', 0))
                if pages_read < 0:
                    raise ValueError("Pages read cannot be negative")

                if book.num_pages and pages_read > book.num_pages:
                    if is_ajax:
                        return JsonResponse({
                            'success': False,
                            'errors': {
                                'pages_read': f'Cannot exceed total pages ({book.num_pages})'
                            }
                        })
                else:
                    book_list.pages_read = pages_read
                    book_list.save()

                    if is_ajax:
                        return JsonResponse({
                            'success': True,
                            'pages_read': book_list.pages_read
                        })
                    return redirect('user_book_info', pk=pk)
            except (ValueError, TypeError) as e:
                if is_ajax:
                    return JsonResponse({
                        'success': False,
                        'errors':
                            {
                                'pages_read': str(e) if "Pages read" in str(e) else 'Invalid page number'
                            }
                    })

        form = BookForm(request.POST, instance=book_list)
        if form.is_valid():
            form.save()
            return redirect('user_book_info', pk=pk)
    else:
        form = BookForm(instance=book_list)

    context = {
        'form': form,
        'book_list': book_list,
        'book': book,
    }
    return render(request, 'user_book_info.html', context)


@login_required()
def delete_book(request, pk):
    book_instance = BookList.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        book_instance.delete()
        return redirect('user_list')
    return render(request, 'user_book_info.html', {'book': book_instance})


@login_required()
@require_http_methods(["GET", "POST"])
def toggle_favourite(request, pk):
    book_list = get_object_or_404(BookList, pk=pk, user=request.user)
    book_list.favourites = not book_list.favourites
    book_list.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_favourite': book_list.favourites
        })

    return redirect('user_book_info', pk=pk)
