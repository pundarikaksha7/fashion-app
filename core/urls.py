from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='index'),
    path('for-you/', views.for_you_view, name='for_you'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('follow', views.follow, name='follow'),
    path('search', views.search, name='search'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post', views.like_post, name='like-post'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('logout', views.logout, name='logout'),
    path('comment/<str:post_id>/', views.add_comment, name='add-comment'),
    path('save-post/<str:post_id>/', views.save_post, name='save-post'),
    path('saved/', views.saved_posts_view, name='saved-posts'),
    path('api/posts/', views.api_posts),
    path('api/profile/<str:username>/', views.api_profile),
    path('api/profile/<str:username>/posts/', views.api_profile_posts),
    path('api/saved/', views.api_saved_posts),
    path('api/foryou/', views.api_for_you),
    path('api/search/', views.api_search),

]