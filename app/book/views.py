from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Book
from django.core.paginator import Paginator


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
