from django.contrib import admin

from api.models import Comment, Post


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'text',
        'pub_date',
        'author'
    )
    list_editable = ('name',)
    search_fields = ('name', 'author')
    list_filter = ('pub_date',)
    empty_value_display = '-empty-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'parent',
        'main_parent',
        'level',
        'created',
        'author',
        'post'
    )
    list_editable = ('post',)
    search_fields = ('text', 'author', 'parent')
    empty_value_display = '-empty-'


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
