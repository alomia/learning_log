from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Topic, Entry


class HomePageView(TemplateView):
    template_name = "home.html"


class TopicListView(LoginRequiredMixin, ListView):
    model = Topic
    template_name = "topic_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topic_list"] = Topic.objects.filter(author=self.request.user)
        return context


class TopicDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Topic
    template_name = "topic_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = Entry.objects.filter(topic=self.kwargs["pk"]).order_by('-date_added')
        return context
    
    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ["title"]
    template_name = "topic_new.html"
    success_url = reverse_lazy("topic_list")
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["title"].label = ""
        return form
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Topic
    template_name = "topic_delete.html"
    success_url = reverse_lazy("topic_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class EntryCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Entry
    fields = ["text"]
    template_name = "entry_new.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = Topic.objects.get(id=self.kwargs["pk"])
        context["topic"] = topic
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["text"].label = ""
        return form
    
    def form_valid(self, form):
        form.instance.topic = Topic.objects.get(id=self.kwargs["pk"])
        return super().form_valid(form)
    
    def test_func(self):
        obj = self.get_object()
        return obj.topic.author == self.request.user


class EntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    fields = ["text"]
    template_name = "entry_edit.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["text"].label = ""
        return form
    
    def test_func(self):
        obj = self.get_object()
        return obj.topic.author == self.request.user


class EntryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entry
    template_name = "entry_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.topic.author == self.request.user


class EntryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = "entry_delete.html"
    
    def get_success_url(self):
        pk = Entry.objects.get(id=self.kwargs["pk"]).topic.pk
        return reverse_lazy("topic_detail", kwargs={"pk": pk})
    
    def test_func(self):
        obj = self.get_object()
        return obj.topic.author == self.request.user
