from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from main.forms import NewsLetterForm, ClientForm, MessageForm
from main.models import NewsLetter, Client, Message


class NewsLetterListView(ListView):
    model = NewsLetter
    template_name = 'main/index.html'


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('main:index')
    login_url = '/user'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:index')
    login_url = '/user'

    def form_valid(self, form):
        if self.request.user != NewsLetter.objects.get(id=self.kwargs.get('pk')).user:
            raise Http404
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


class MyNewsLetterListView(LoginRequiredMixin, ListView):
    model = NewsLetter
    template_name = 'main/my_newsletter_list.html'
    login_url = '/user'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = NewsLetter.objects.filter(user=self.request.user)

        return context_data


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetter
    form_class = NewsLetterForm
    success_url = reverse_lazy('main:index')
    login_url = '/user'

    def form_valid(self, form):
        if self.request.user != NewsLetter.objects.get(id=self.kwargs.get('pk')).user:
            raise Http404

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user != NewsLetter.objects.get(id=self.kwargs.get('pk')).user:
            raise Http404
        return super().get(request, *args, **kwargs)


class NewsLetterDeleteView(DeleteView):
    model = NewsLetter
    template_name = 'main/newsletter_delete.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        if self.request.user != NewsLetter.objects.get(id=self.kwargs.get('pk')).user:
            raise Http404

        return super().form_valid(form)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.newsletter_id = self.kwargs.get('pk')
        self.object.save()
        return super().form_valid(form)
