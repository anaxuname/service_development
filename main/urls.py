from django.urls import path

from main.apps import MainConfig
from main.views import NewsLetterListView, NewsLetterCreateView, NewsLetterDetailView, NewsLetterUpdateView, \
    AccessDeniedView, ClientCreateView

app_name = MainConfig.name


urlpatterns = [
    path('', NewsLetterListView.as_view(), name='index'),
    path('create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/<int:pk>', NewsLetterDetailView.as_view(), name='newsletter_detail'),
    path('update/<int:pk>', NewsLetterUpdateView.as_view(), name='newsletter_update'),
    path('subscribe/<int:pk>', ClientCreateView.as_view(), name='client_create'),
    path('denied/', AccessDeniedView.as_view(), name='main_access_denied'),
]
