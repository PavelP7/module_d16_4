from django.contrib import admin
from .models import Post, Comment, Author, Category

class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'text', 'datetime_in', 'rating')
    list_filter = ('author', 'datetime_in', 'rating')
    search_fields = ('title', 'text')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Author)
admin.site.register(Category)

admin.site.unregister(Comment)
