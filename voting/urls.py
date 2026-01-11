from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.PollDetailView.as_view(), name='poll_detail'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]
