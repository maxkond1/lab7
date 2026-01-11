from django.urls import path
from . import api_views

urlpatterns = [
    path('polls/', api_views.PollListAPI.as_view()),
    path('polls/<int:pk>/', api_views.PollDetailAPI.as_view()),
    path('votes/', api_views.VoteCreateAPI.as_view()),
]
