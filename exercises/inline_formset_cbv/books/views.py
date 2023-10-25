from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import Author
from .forms import AuthorBooksFormset


class HomeView(TemplateView):
    template_name = "home.html"


class AuthorListView(ListView):
    template_name = "author_list.html"
    model = Author
    context_object_name = "authors"


class AuthorDetailView(DetailView):
    template_name = "author_detail.html"
    model = Author


class AuthorCreateView(CreateView):
    template_name = "author_create.html"
    model = Author
    fields = ("name",)

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "The author has been added")

        return super().form_valid(form)


class AuthorBooksEditView(SingleObjectMixin, FormView):
    template_name = "author_book_edit.html"
    model = Author

    def get(self, *args, **kwargs):
        self.object = self.get_object(queryset=Author.objects.all())

        return super().get(*args, *kwargs)

    def post(self, *args, **kwargs):
        self.object = self.get_object(queryset=Author.objects.all())

        return super().post(*args, **kwargs)

    def get_form(self, form_class=None):
        return AuthorBooksFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Changes were saved")
        super().form_valid(form)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("books:author_detail", kwargs={"pk": self.object.pk})
