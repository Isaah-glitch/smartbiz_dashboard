# smartbiz_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),            # Auth pages
    path('', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),  # Dashboard pages
]
