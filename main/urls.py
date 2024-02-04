from django.urls import path

from main.apps import MainConfig
from main.views import NewsLetterListView, NewsLetterCreateView, NewsLetterDetailView, NewsLetterUpdateView, \
    ClientCreateView, MessageCreateView, NewsLetterDeleteView, \
    MyNewsLetterListView

app_name = MainConfig.name

urlpatterns = [
    path('', NewsLetterListView.as_view(), name='index'),
    path('create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('message/<int:pk>/create', MessageCreateView.as_view(), name='message_create'),
    path('newsletter/<int:pk>/delete', NewsLetterDeleteView.as_view(), name='newsletter_delete'),
    path('newsletter/<int:pk>', NewsLetterDetailView.as_view(), name='newsletter_detail'),
    path('my_newsletter/', MyNewsLetterListView.as_view(), name='my_newsletter_list'),
    path('newsletter/<int:pk>/update', NewsLetterUpdateView.as_view(), name='newsletter_update'),
    path('subscribe/<int:pk>', ClientCreateView.as_view(), name='client_create'),
]
