import re
from urllib.parse import quote

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Value, Q
from django.db.models.functions import Coalesce
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, RedirectView
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormView

from hasker.core.forms import CreateQuestionForm, CreateAnswerForm
from hasker.core.models import Question, Tag


class MainPageView(ListView):
    template_name = 'core/main_page.html'
    paginate_by = 20
    model = Question
    context_object_name = 'questions'
    ordering = '-created_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordering_tag = self.request.GET.get('order_by')
        if ordering_tag == 'hot':
            context['ordering'] = 'hot'
        else:
            context['ordering'] = 'new'
        return context

    def get_queryset(self):
        ordering_tag = self.request.GET.get('order_by')
        queryset = super().get_queryset()
        if ordering_tag == 'hot':
            queryset = queryset.annotate(
                votes_rating=Coalesce(Sum('votes__value'), Value(0))
            ).order_by('-votes_rating')
        return queryset


class CreateQuestionView(LoginRequiredMixin, CreateView):
    template_name = 'core/ask.html'
    success_url = '/'
    form_class = CreateQuestionForm
    model = Question

    def form_valid(self, form):
        question_obj = form.save(commit=False)
        question_obj.author = self.request.user
        question_title = form.cleaned_data['title']
        question_obj.slug = slugify(question_title)[:49]
        question_obj.save()
        raw_tags = form.cleaned_data['tags']
        for raw_tag in raw_tags.split(','):
            if raw_tag:
                tag_obj, _ = Tag.objects.get_or_create(name=raw_tag.strip())
                question_obj.tags.add(tag_obj)
        return redirect('question', slug=question_obj.slug)


class CreateAnswerView(SingleObjectMixin, FormView):
    template_name = 'core/question.html'
    form_class = CreateAnswerForm
    model = Question

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        answer_obj = form.save(commit=False)
        answer_obj.author = self.request.user
        answer_obj.question = self.object
        answer_obj.save()
        return redirect('question', slug=self.kwargs['slug'])


class QuestionDetailView(DetailView):
    template_name = 'core/question.html'
    model = Question
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CreateAnswerForm()
        return context


class QuestionView(View):
    def get(self, request, *args, **kwargs):
        view = QuestionDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CreateAnswerView.as_view()
        return view(request, *args, **kwargs)


class SearchView(ListView):
    template_name = 'core/search.html'
    paginate_by = 20
    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(text__icontains=query)
            ).annotate(
                votes_rating=Coalesce(Sum('votes__value'), Value(0))
            ).order_by('-votes_rating', '-created_at')
        return queryset


class TagView(ListView):
    template_name = 'core/tags.html'
    paginate_by = 20
    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(tags__name=self.kwargs.get('name'))


class SearchRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        input_string = self.request.POST.get('search')
        parsed_input = re.match(r'tag:(\w+)', input_string)
        if parsed_input:
            tag_name = parsed_input.group(1)
            return reverse('tag', args=(tag_name, ))
        search_url = '{}?q={}'.format(reverse('search'), input_string)
        return quote(search_url, safe='/?=')
