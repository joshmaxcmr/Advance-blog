
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('blog.urls')),  # URLs du blog à la racine aussi
]
