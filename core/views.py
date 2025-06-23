from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Profile, Post, LikePost, FollowersCount, Comment
from itertools import chain
import random
from django.core.files.base import ContentFile
import base64
import uuid 
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from .models import Post, Comment, SavedPost
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Profile, Post, LikePost, FollowersCount, Comment, SavedPost, PostMedia
from itertools import chain

@login_required(login_url='signin')
def api_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'image': post.image.url if post.image else '',
            'username': post.user,
        })
    return JsonResponse(data, safe=False)

@login_required(login_url='signin')
def api_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return JsonResponse({
        'username': user.username,
        'name': user.username,  # Replace with actual name if stored
        'bio': profile.bio,
        'location': profile.location,
        'profileimg': profile.profileimg.url if profile.profileimg else '',
    })

@login_required(login_url='signin')
def api_profile_posts(request, username):
    posts = Post.objects.filter(user=username).order_by('-created_at')
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'image': post.image.url if post.image else '',
        })
    return JsonResponse(data, safe=False)

@login_required(login_url='signin')
def api_saved_posts(request):
    saved = SavedPost.objects.filter(user=request.user).order_by('-saved_at')
    data = []
    for entry in saved:
        post = entry.post
        data.append({
            'id': post.id,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'image': post.image.url if post.image else '',
        })
    return JsonResponse(data, safe=False)

@login_required(login_url='signin')
def api_for_you(request):
    all_posts = Post.objects.exclude(user=request.user.username).order_by('-created_at')
    suggestions = []
    for post in all_posts:
        suggestions.append({
            'id': post.id,
            'text': f"Check out this post by {post.user}",
        })
    return JsonResponse(suggestions, safe=False)

@login_required(login_url='signin')
def api_search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse([], safe=False)

    matched_users = User.objects.filter(username__icontains=query)
    matched_posts = Post.objects.filter(caption__icontains=query)

    results = []
    for user in matched_users:
        results.append({
            'id': f'user-{user.id}',
            'username': user.username
        })
    for post in matched_posts:
        results.append({
            'id': f'post-{post.id}',
            'caption': post.caption,
            'image': post.image.url if post.image else '',
        })

    return JsonResponse(results, safe=False)

####################### API SECTION OVER ##########################


@login_required(login_url='signin')
def add_comment(request,post_id):
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        # post_id = request.GET.get('post_id')

        # if not post_id or not text:
        #     return HttpResponseBadRequest("Missing post_id or comment_text.")

        post = get_object_or_404(Post, id=post_id)

        Comment.objects.create(post=post, user=request.user, text=text)

        # Redirect to the referring page
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return HttpResponseBadRequest("Invalid request method.")



@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list = list(chain(*feed))

    for post in feed_list:
        post.liked_by = list(LikePost.objects.filter(post_id=post.id).values_list('username', flat=True))


    #  # Add comments to each post
    # for post in feed_list:
    #     post.comments = Comment.objects.filter(post=post)

    # user suggestion starts
    all_users = User.objects.all()
    user_following_all = []

    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))


    return render(request, 'index.html', {'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        caption = request.POST.get('caption', '')
        cropped_data_list = request.POST.getlist('cropped_image_data')  # base64 images
        media_files = request.FILES.getlist('media')  # uploaded files

        if not cropped_data_list and not media_files:
            messages.error(request, 'No media provided.')
            return render(request, 'upload.html')

        post = Post.objects.create(user=request.user.username, caption=caption)

        # Handle cropped base64 images
        for cropped_data in cropped_data_list:
            if cropped_data:
                format, imgstr = cropped_data.split(';base64,') 
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
                PostMedia.objects.create(post=post, file=data, is_image=True)

        # Handle uploaded files
        for file in media_files:
            is_image = file.content_type.startswith('image')
            PostMedia.objects.create(post=post, file=file, is_image=is_image)

        messages.success(request, 'Post created successfully.')
        return redirect('index')

    return render(request, 'upload.html')

@login_required(login_url='signin')
def for_you_view(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    all_posts = Post.objects.exclude(user=user_profile).order_by('-created_at')  # or whatever your logic is

    for post in all_posts:
        liked_users = LikePost.objects.filter(post_id=post.id).values_list('username', flat=True)
        post.liked_by = list(liked_users)
        post.is_liked_by_user = request.user.username in post.liked_by

    return render(request, 'for_you.html', {
        'user_profile': user_profile,
        'posts': all_posts
    })

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        # return JsonResponse({'success': True, 'new_like_count': post.no_of_likes, 'liked': True})
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    for post in user_posts:
        post.liked_by = list(LikePost.objects.filter(post_id=post.id).values_list('username', flat=True))


     # Add comments to each post
    # for post in user_posts:
    #     post.comments = Comment.objects.filter(post=post)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Check if the post is already saved
    if SavedPost.objects.filter(user=user, post=post).exists():
        SavedPost.objects.filter(user=user, post=post).delete() #Unsave post if already saved
    else:
        SavedPost.objects.create(user=user, post=post)

    return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to the previous page
    
@login_required(login_url='signin')
def saved_posts_view(request):
    user = request.user
    saved_posts = SavedPost.objects.filter(user=user).order_by('-saved_at')
        
    # Fetch the actual Post objects from the SavedPost instances
    posts = [saved_post.post for saved_post in saved_posts]

    # Add liked_by attribute to each post (similar to index view)
    for post in posts:
        post.liked_by = list(LikePost.objects.filter(post_id=post.id).values_list('username', flat=True))

    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    return render(request, 'saved_posts.html', {'posts': posts, 'user_profile': user_profile})
    