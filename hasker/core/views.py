from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DetailView, ListView
from django.utils.text import slugify
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin, FormView

from hasker.core.forms import CreateQuestionForm, CreateAnswerForm
from hasker.core.models import Question, Tag, Answer


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
            pass
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
        question_obj.slug = slugify(question_title)
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
