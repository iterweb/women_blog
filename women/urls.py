from django.urls import path

from women.views import *


urlpatterns = [
    # path('post/<slug:post_slug>/', show_post, name='post'),
    path('post/<slug:post_slug>/', ShowPostView.as_view(), name='post'),
    # path('category/<slug:cat_slug>/', show_category, name='category'),
    path('category/<slug:cat_slug>/', ShowCategoryView.as_view(), name='category'),
    # path('about/', about, name='about'),
    path('about/', AboutView.as_view(), name='about'),
    # path('add/', add, name='add_post'),
    path('add/', AddPostView.as_view(), name='add_post'),
    # path('contact/', contact, name='contact'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('search/', SearchView.as_view(), name='search'),
    path('like/', like_post, name='like_post'),
    path('comment/<int:pk>/', AddComment.as_view(), name="add_comment"),
    # path('', index, name='home'),
    path('', IndexView.as_view(), name='home'),
]