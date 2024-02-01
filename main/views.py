from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView, DeleteView

from main.forms import NewsLetterForm, ClientForm, MessageForm
from main.models import NewsLetter, Client, Message


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'main/index.html'


class MyNewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous:
            context['object_list'] = context['object_list'].filter(user=self.request.user)
        return context


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('main:index')


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.newsletter_id = self.kwargs.get('pk')
        self.object.save()
        return super().form_valid(form)

class NewsLetterDetailView(DetailView):
    model = NewsLetter
    template_name = 'main/newsletter.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        messages = Message.objects.filter(newsletter=self.object)
        context_data['messages'] = messages
        return context_data


class MyNewsLetterDetailView(DetailView):
    """
    May be used in the future
    """
    model = NewsLetter
    template_name = 'main/my_newsletter.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        messages = Message.objects.filter(newsletter=self.object)
        context_data['messages'] = messages
        return context_data

class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('main:index')


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    template_name = 'main/newsletter_delete.html'
    success_url = reverse_lazy('main:index')

class AccessDeniedView(TemplateView):
    template_name = 'main /form_redirect.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:index')
