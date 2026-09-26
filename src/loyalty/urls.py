from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/search/', views.search_clients, name='search_clients'),
    path('api/action/', views.handle_action, name='handle_action'),
    path('api/create/', views.create_client_inline, name='create_client_inline'),
]