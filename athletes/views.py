from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib import messages

from .forms import AddAthleteForm, ShareAthleteEmailForm, CommentForm
from .models import Athlete, Category, Comment


class AthletesListView(ListView):
    template_name = 'athletes/index.html'
    context_object_name = 'athletes'
    queryset = Athlete.objects.all().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Athletes'
        return context


class AthleteDetailView(DetailView, FormView):
    model = Athlete
    template_name = 'athletes/detail.html'
    context_object_name = 'athlete'
    slug_url_kwarg = 'athlete_slug'
    form_class = CommentForm

    def get_queryset(self):
        return super().get_queryset().select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = context['athlete'].title
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.athlete = self.get_object()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'athlete_slug': self.kwargs['athlete_slug']})


class CategoryAthletesListView(ListView):
    model = Athlete
    context_object_name = 'athletes'
    template_name = "athletes/category.html"
    paginate_by = 3
    allow_empty = False

    def get_queryset(self):
        slug = self.kwargs['cat_slug']
        return Athlete.objects.filter(category__slug=slug, is_published=True).select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = context['athletes'][0].category.name
        return context


class NewAthlete(LoginRequiredMixin, CreateView):
    form_class = AddAthleteForm
    success_url = reverse_lazy('index')
    template_name = 'athletes/add_athlete.html'
    extra_context = {
        'title': 'Добавление статьи'
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class SearchAthlete(SuccessMessageMixin, ListView):
    model = Athlete
    template_name = 'athletes/search_athlete.html'
    context_object_name = 'athletes'

    def get_queryset(self):
        search_query = self.request.GET['search']
        return Athlete.objects.filter(title__regex=fr'(?i){search_query}').select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = f"Поиск - {self.request.GET['search']}"
        return context


def post_share(request, athlete_slug):
    post = get_object_or_404(Athlete, slug=athlete_slug)
    sent = False
    if request.method == 'POST':
        form = ShareAthleteEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comment: {cd['comment']}"
            send_mail(subject, message, cd['sender'], [cd['to']])
            sent = True
    else:
        form = ShareAthleteEmailForm()
    context = {'post': post,
               'form': form,
               'sent': sent}
    return render(request, 'athletes/share.html', context)


@login_required
@require_POST
def athlete_like(request):
    athlete_id = request.POST.get('id')
    action = request.POST.get('action')
    if athlete_id and action:
        try:
            athlete = Athlete.objects.get(pk=athlete_id)
            if action == 'like':
                athlete.users_like.add(request.user)
            else:
                athlete.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Athlete.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


class AthletesLikes(LoginRequiredMixin, ListView):
    template_name = 'athletes/likes.html'
    context_object_name = 'athletes'

    def get_queryset(self):
        user = self.request.user
        return Athlete.objects.filter(users_like=user).select_related()
