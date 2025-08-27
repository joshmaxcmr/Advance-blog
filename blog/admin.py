from django.contrib import admin
from .models import Post
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'created', 'updated', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish' #Barre de navigation par date
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS #compteur de filtre
