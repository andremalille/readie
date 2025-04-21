from django.urls import path

from book import views


urlpatterns = [
    path('list/', views.books_view, name='books'),
    path('list/info/<int:pk>/', views.book_info, name='book_info'),
]
