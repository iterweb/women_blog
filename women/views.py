from django.db.models import Q, F
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, TemplateView, FormView, View
from django.core.cache import cache

from .models import Women
from .forms import *
from .utils import *


class IndexView(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        articles = cache.get('articles')
        if not articles:
            articles = Women.objects.filter(is_published=True).select_related('category')
            cache.set('articles', articles, 1)
        return articles

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.user_context(title='Главная')
        return dict(list(context.items()) + list(mixin.items()))


class ShowCategoryView(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        cache_name = self.kwargs['cat_slug']
        articles_in_category = cache.get(cache_name)
        if not articles_in_category:
            articles_in_category = Women.objects.filter(category__slug=self.kwargs['cat_slug'], is_published=True).select_related('category')
            cache.set(cache_name, articles_in_category, 1)
        return articles_in_category

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_selected = self.kwargs['cat_slug']
        title = f'Рубрика | {str(context["posts"][0].category)}'
        mixin = self.user_context(title=title, cat_selected=cat_selected)
        return dict(list(context.items()) + list(mixin.items()))


class ShowPostView(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        title = context['post']
        form = CommentForm
        liked = False
        if context['post'].likes.filter(id=self.request.user.id).exists():
            liked = True
        mixin = self.user_context(title=title, form=form, is_liked=liked)

        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        return dict(list(context.items()) + list(mixin.items()))


def like_post(request):
    post = get_object_or_404(Women, id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    context = {
        'post': post,
        'is_liked': liked,
    }
    if request.is_ajax():
        html = render_to_string('women/inc/_likes.html', context=context, request=request)
        return JsonResponse({'form': html})


class AddPostView(LoginRequiredMixin, DataMixin, CreateView):
    form_class = Add_Post_Form
    template_name = 'women/add_article.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.user_context(title='Добавить пост')
        return dict(list(context.items()) + list(mixin.items()))


class UserRegisterView(DataMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.user_context(title='Регистрация')
        return dict(list(context.items()) + list(mixin.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserLoginView(DataMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.user_context(title='Войти')
        return dict(list(context.items()) + list(mixin.items()))

    def get_success_url(self):
        return reverse_lazy('home')


class SearchView(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        cache_name = self.request.GET.get('q').replace(' ', '_').strip()
        posts_filter = cache.get(cache_name)
        if not posts_filter:
            posts_filter = Women.objects.filter(
                Q(title__icontains=self.request.GET.get('q')) | Q(content__icontains=self.request.GET.get('q'))
            ).select_related('category')
            cache.set(cache_name, posts_filter, 1)
        return posts_filter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = f"q={self.request.GET.get('q').replace(' ', '+').strip()}&"
        mixin = self.user_context(title='Поиск', search=search)
        return dict(list(context.items()) + list(mixin.items()))


class AboutView(DataMixin, TemplateView):
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.user_context(title='О сайте')
        return dict(list(context.items()) + list(mixin.items()))


class ContactView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        mixin = self.user_context(title='Обратная связь')
        return dict(list(context.items()) + list(mixin.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')


class AddComment(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        post = Women.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.post = post
            form.author = request.user
            form.save()
        return redirect(post.get_absolute_url())


def user_logout(request):
    logout(request)
    return redirect('home')

"""
def index(request):
    posts = Women.objects.all()
    context = {
        'title': 'Главная',
        'menu': menu,
        'cat_selected': 0,
        'posts': posts,
    }
    return render(request, 'women/index.html', context=context)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    slug = post.category.slug

    context = {
        'post': post,
        'menu': menu,
        'cat_selected': slug
    }
    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    posts = Women.objects.filter(category__slug=cat_slug)

    if len(posts) == 0:
        raise Http404()

    context = {
        'title': 'Рубрика',
        'menu': menu,
        'cat_selected': cat_slug,
        'posts': posts,
    }
    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})

def add(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            try:
                Women.objects.create(**form.cleaned_data)
                return redirect('home')
            except:
                form.add_error(None, 'Ошибка добавления')
    else:
        form = AddPostForm()

    context = {
        'title': 'Добавить пост',
        'menu': menu,
        'form': form
    }
    return render(request, 'women/add_article.html', context=context)


def add(request):
    if request.method == 'POST':
        form = Add_Post_Form(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('home')
    else:
        form = Add_Post_Form()

    context = {
        'title': 'Добавить пост',
        'menu': menu,
        'form': form
    }
    return render(request, 'women/add_article.html', context=context)


def contact(request):
    return HttpResponse(f'<h1>Контакты</h1>')
"""

def pageNotFound(request, exception):
    return HttpResponseNotFound(f'<h1>Page Not Found</h1><p>---!!!---</p>')
