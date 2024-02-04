from django.contrib import admin

from main.models import Client, NewsLetter, Message


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_mailing', 'periodicity_mailing', 'user')
    list_filter = ('name', )
    search_fields = ('name', 'user')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status_mailing', 'newsletter')
    search_fields = ('title',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'newsletter')
    search_fields = ('full_name', 'newsletter')
