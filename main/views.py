from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView

from main.forms import NewsLetterForm, ClientForm
from main.models import NewsLetter, Client


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'main/index.html'


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('main:index')


class NewsLetterDetailView(DetailView):
    model = NewsLetter
    template_name = 'main/newsletter.html'

class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('main:index')


class AccessDeniedView(TemplateView):
    template_name = 'main /form_redirect.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:index')
