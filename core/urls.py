from django.urls import path
from . import views

urlpatterns = [
    # Auth endpoints
    path('api/signup/', views.api_signup, name='api-signup'),
    path('api/signin/', views.api_signin, name='api-signin'),
    path('api/logout/', views.api_logout, name='api-logout'),

    # Example: include all other API endpoints here
    path('api/posts/', views.api_posts, name='api-posts'),
    path('api/profile/<str:username>/', views.api_profile, name='api-profile'),
    path('api/profile/<str:username>/posts/', views.api_profile_posts, name='api-profile-posts'),
    path('api/saved/', views.api_saved_posts, name='api-saved-posts'),
    path('api/foryou/', views.api_for_you, name='api-foryou'),
    path('api/search/', views.api_search, name='api-search'),
    path('api/comment/<str:post_id>/', views.api_add_comment, name='api-add-comment'),
    path('api/like/', views.api_like_post, name='api-like-post'),
    path('api/save/<str:post_id>/', views.api_save_post, name='api-save-post'),
    path('api/follow/', views.api_follow, name='api-follow'),
    path('api/settings/', views.api_settings, name='api-settings'),
    path('api/upload/', views.api_upload, name='api-upload'),
]
