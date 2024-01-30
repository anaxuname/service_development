from django.contrib import admin

from main.models import Client, NewsLetter


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_mailing', 'status_mailing', 'user')
    list_filter = ('name', 'status_mailing')
    search_fields = ('name', 'user')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name')
    search_fields = ('full_name', 'newsletter')