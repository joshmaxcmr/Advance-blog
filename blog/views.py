from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PostListView(ListView):
    """
    Vue basée sur une classe pour afficher la liste des posts publiés
    """
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 5
    
    def get_queryset(self):
        """Retourne seulement les posts publiés, ordonnés par date de publication"""
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liste des Articles'
        return context


class PostDetailView(DetailView):
    """
    Vue basée sur une classe pour afficher le détail d'un post
    """
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Retourne seulement les posts publiés"""
        return Post.objects.filter(status=Post.Status.PUBLISHED)
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


# Vue fonction alternative pour la liste des posts
def post_list(request):
    """
    Vue fonction pour afficher la liste des posts avec pagination
    """
    post_list = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')
    paginator = Paginator(post_list, 5)  # 5 posts par page
    page_number = request.GET.get('page', 1)
    
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/post_list.html', {'posts': posts})


# Vue fonction pour le détail d'un post
def post_detail(request, year, month, day, slug):
    """
    Vue fonction pour afficher le détail d'un post par date et slug
    """
    post = get_object_or_404(Post,
                           status=Post.Status.PUBLISHED,
                           publish__year=year,
                           publish__month=month,
                           publish__day=day,
                           slug=slug)
    
    return render(request, 'blog/post_detail.html', {'post': post})