from blog.models import Blog


class ModeratorBlogForm:
    class Meta:
        model = Blog
        fields = ('title', 'body', 'data_create', 'count_views',)
