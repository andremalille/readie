from django.urls import path

from user import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register/name/', views.user_name_view, name='name'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('change-info/', views.change_info_view, name='change_info'),
]
