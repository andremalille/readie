from django.urls import path

from book import views


urlpatterns = [
    path('list/', views.books_view, name='books'),
    path('list/info/<int:pk>/', views.book_info, name='book_info'),
    path(
        'list/info/add/<int:pk>',
        views.book_add_to_list,
        name='add_book'
    ),
    path('list/user/', views.book_user_list, name='user_list'),
    path(
        'list/user/info/<int:pk>/',
        views.user_book_info,
        name='user_book_info'
    ),
    path('edit-book/<int:pk>/', views.edit_book_view, name='edit_book'),
    path('delete-book/<int:pk>/', views.delete_book, name='delete_book'),
]
