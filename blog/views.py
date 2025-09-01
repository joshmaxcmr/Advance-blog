from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .forms import EmailPostForm
from django.core.mail import send_mail


class PostListView(ListView):
  
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    
    def get_queryset(self):
        """Retourne seulement les posts publiés, ordonnés par date de publication"""
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liste des Articles'
        return context
    
    def paginate_queryset(self, queryset, page_size):
        """
        Gère la pagination avec gestion des erreurs EmptyPage et PageNotAnInteger
        """
        paginator = self.get_paginator(
            queryset, page_size, orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty()
        )
        
        page = self.kwargs.get(self.page_kwarg) or self.request.GET.get(self.page_kwarg) or 1
        
        try:
            page_number = int(page)
        except (TypeError, ValueError):
            raise Http404("Numéro de page invalide.")
        
        try:
            page_obj = paginator.page(page_number)
            return paginator, page_obj, page_obj.object_list, page_obj.has_other_pages()
        except PageNotAnInteger:
            # Si le numéro de page n'est pas un entier, afficher la première page
            page_obj = paginator.page(1)
            return paginator, page_obj, page_obj.object_list, page_obj.has_other_pages()
        except EmptyPage:
            # Si la page est vide (au-delà de la dernière page), afficher la dernière page
            page_obj = paginator.page(paginator.num_pages)
            return paginator, page_obj, page_obj.object_list, page_obj.has_other_pages()


class PostDetailView(DetailView):
  
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        """
        Récupère l'objet Post en utilisant les paramètres year, month, day et post (slug)
        Cette méthode est nécessaire car l'URL contient plusieurs paramètres de date
        """
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=self.kwargs['post'],
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day']
        )
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte"""
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']],
            )
            sent = True

    else:
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        },
    )
