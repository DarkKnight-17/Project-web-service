
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home' ),
    path('search',views.search, name = 'search' ),
    path('add_newcar/', views.add_newcar, name='add_newcar'),
    path('edit_car/<str:pk>/', views.update_car, name = 'update_car'),
    path('delete_car/<str:pk>/', views.delete_car, name = 'delete_car'),
    path('Login/', views.loginPage, name = 'login'),
    path('Logout/', views.logoutUser, name = 'logout'),
    path('Register/', views.registerPage, name = 'register')
]