from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login, name='login'),
    path('admin/users', views.get_all_users, name='getUsers'),
    path('admin/create-user', views.create_user, name='createUser'),
    path('admin/users/id/<int:id>', views.user_management, name='userManagement')
]
