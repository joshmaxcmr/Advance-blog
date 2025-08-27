from django.urls import path
from . import views

app_name = 'blog' #name space pour éviter conflits avec les autres applications 

urlpatterns = [
    # URLs pour les vues basées sur des classes
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail')
    ]
    
  