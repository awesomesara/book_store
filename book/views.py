from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from .forms import *
from .models import *
from django.contrib import messages


class MainPageView(ListView):
    model = BooksModel
    template_name = 'index.html'
    context_object_name = 'books'
    paginate_by = 2


class AuthorDetailView(DetailView):
    model = AuthorModel
    template_name = 'author-detail.html'
    context_object_name = 'author'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = BooksModel.objects.filter(author_id=self.slug)
        return context

class BookDetailView(DetailView):
    model = BooksModel
    template_name = 'book-detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object().get_image
        context['images'] = self.get_object().images.exclude(id=image.id)
        return context


def add_book(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        book_form = BookForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if book_form.is_valid() and formset.is_valid():
            book = book_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, book=book)
            return redirect(book.get_absolute_url())
    else:
        recipe_form = BookForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-book.html', locals())


class DeleteBookView(DeleteView):
    model = BooksModel
    template_name = 'delete-book.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return HttpResponseRedirect(success_url)
