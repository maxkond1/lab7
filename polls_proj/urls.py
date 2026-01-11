from django.contrib import admin
from django.urls import path, include
from voting import views as voting_views
from voting.admin_views import export_xlsx

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/export-xlsx/', export_xlsx, name='admin_export_xlsx'),
    path('', voting_views.PollListView.as_view(), name='poll_list'),
    path('polls/', include('voting.urls')),
    path('api/', include('voting.api_urls')),
]
