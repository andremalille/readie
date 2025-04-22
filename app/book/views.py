from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # noqa
from core.models import Book, BookList
from django.core.paginator import Paginator
from book.forms import BookForm


def books_view(request):
    books_list = Book.objects.all().order_by('title')

    paginator = Paginator(books_list, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'book_list.html', context)


def book_info(request, pk):
    book = Book.objects.get(pk=pk)

    context = {'book': book}
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
    books_list = BookList.objects.filter(user=request.user).order_by('book')

    paginator = Paginator(books_list, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'user_list.html', context)


def user_book_info(request, pk):
    book_list_instance = BookList.objects.get(pk=pk)
    book = book_list_instance.book

    context = {'book': book, 'book_list': book_list_instance}
    return render(request, 'user_book_info.html', context)


def edit_book_view(request, pk):
    book_instance = BookList.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book_instance)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = BookForm(instance=book_instance)
    context = {'form': form, 'book': book_instance}

    return render(request, 'edit_book.html', context)


def delete_book(request, pk):
    book_instance = BookList.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        book_instance.delete()
        return redirect('user_list')
    return render(request, 'delete_book.html', {'book': book_instance})
