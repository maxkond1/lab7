from django.contrib import admin
from django.urls import path, include
from voting import views as voting_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', voting_views.PollListView.as_view(), name='poll_list'),
    path('polls/', include('voting.urls')),
    path('api/', include('voting.api_urls')),
]
