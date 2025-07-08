from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import Profile, Post, LikePost, FollowersCount, Comment, SavedPost, PostMedia,DirectMessage, ApparelTag
from .serializers import DirectMessageSerializer
from django.db.models import Q
from django.core.files.base import ContentFile
import base64, uuid,os
import os
from collections import Counter 
import difflib
from unidecode import unidecode



from .ml import detect_apparel,is_obscene



# Send a message
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    recipient_username = request.data.get('recipient')
    message_text = request.data.get('message')

    if not recipient_username or not message_text:
        return Response({'error': 'Recipient and message are required.'}, status=status.HTTP_400_BAD_REQUEST)

    recipient = get_object_or_404(User, username=recipient_username)
    message = DirectMessage.objects.create(sender=request.user, recipient=recipient, message=message_text)
    serializer = DirectMessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

# Get chat history with a user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation(request, username):
    other_user = get_object_or_404(User, username=username)

    messages = DirectMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) |
        (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('timestamp')

    serializer = DirectMessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def api_signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password2 = request.data.get('password2')

    if not all([username, email, password, password2]):
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
        return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)

    Profile.objects.create(
        user=user,
        id_user=user.id,
        name=request.data.get('name', ''),
        age=request.data.get('age'),
        gender=request.data.get('gender', ''),
        occupation=request.data.get('occupation', ''),
        college=request.data.get('college', ''),
        city=request.data.get('city', ''),
        state=request.data.get('state', ''),
        fashion_preferences=request.data.get('fashion_preferences', ''),
        color_preferences=request.data.get('color_preferences', ''),
    )

    return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def api_signin(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful.'})
    return Response({'error': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    logout(request)
    return Response({'message': 'Logged out successfully.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_settings(request):
    profile = Profile.objects.get(user=request.user)

    # Basic fields
    profile.bio = request.data.get('bio', profile.bio)

    # New fields
    profile.name = request.data.get('name', profile.name)
    profile.age = request.data.get('age', profile.age)
    profile.gender = request.data.get('gender', profile.gender)
    profile.occupation = request.data.get('occupation', profile.occupation)
    profile.college = request.data.get('college', profile.college)
    profile.city = request.data.get('city', profile.city)
    profile.state = request.data.get('state', profile.state)
    profile.fashion_preferences = request.data.get('fashion_preferences', profile.fashion_preferences)
    profile.color_preferences = request.data.get('color_preferences', profile.color_preferences)

    # Image
    image = request.FILES.get('image')
    if image:
        profile.profileimg = image

    profile.save()
    return Response({'message': 'Profile updated successfully.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_follow(request):
    user = request.data.get('user')
    follower = request.user.username

    if FollowersCount.objects.filter(follower=follower, user=user).exists():
        FollowersCount.objects.filter(follower=follower, user=user).delete()
        return Response({'message': 'Unfollowed'})
    FollowersCount.objects.create(follower=follower, user=user)
    return Response({'message': 'Followed'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_upload(request):
    caption = request.data.get('caption', '')
    media_files = request.FILES.getlist('media')

    print("FILES RECEIVED:", request.FILES)
    print("MEDIA FILES:", media_files)

    if not media_files:
        return Response({'error': 'No media provided.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create Post
    post = Post.objects.create(user=request.user.username, caption=caption)

    # Save uploaded media
    for file in media_files:
        is_image = file.content_type.startswith('image')
        PostMedia.objects.create(post=post, file=file, is_image=is_image)

         # Obscenity check
        if is_image and is_obscene(file):
            post.delete()
            return Response({
                'error': 'Obscene content detected. Post rejected.',
                'details': f'Objectionable image: {file.name}'
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            print("No obscene content detected")

    # Apparel detection
    image_apparel_map = {}
    apparel_detected = False

    for media in post.media_files.all():
        if not media.is_image:
            continue

        file_path = media.file.path
        if not os.path.isfile(file_path):
            continue

        labels = detect_apparel(file_path)  # Detect clothing items with attributes

        for result in labels:
            label = result['label']
            confidence = result.get('confidence', 0)
            color = result.get('color')
            item = result.get('item')
            print("CONFIDENCE:", confidence)

            image_apparel_map.setdefault(label, []).append(media.file.url)

            ApparelTag.objects.create(
                post=post,
                image=media,
                label=label,
                confidence=confidence,
                color=color,
                item=item
            )

        if labels:
            apparel_detected = True

    # Update post flag
    post.is_apparel = apparel_detected
    post.save()

    if not apparel_detected:
        return Response({
            'warning': 'No apparel detected in uploaded images.',
            'suggestion': 'You may want to edit your post to include fashion-related content.',
            'post_id': str(post.id),
            'apparel_map':image_apparel_map
        }, status=status.HTTP_202_ACCEPTED)

    return Response({
        'message': 'Post created and analyzed.',
        'post_id': str(post.id),
        'apparel_map': image_apparel_map
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if SavedPost.objects.filter(user=request.user, post=post).exists():
        SavedPost.objects.filter(user=request.user, post=post).delete()
        return Response({'message': 'Post unsaved'})
    SavedPost.objects.create(user=request.user, post=post)
    return Response({'message': 'Post saved'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_comment(request, post_id):
    text = request.data.get('comment_text')
    post = get_object_or_404(Post, id=post_id)
    Comment.objects.create(post=post, user=request.user, text=text)
    return Response({'message': 'Comment added'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_like_post(request):
    post_id = request.data.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    username = request.user.username

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter is None:
        LikePost.objects.create(post_id=post_id, username=username)
        post.no_of_likes += 1
        post.save()
        return Response({'message': 'Liked'})
    like_filter.delete()
    post.no_of_likes -= 1
    post.save()
    return Response({'message': 'Unliked'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_posts(request):
    # Get all users followed by the current user
    followed_usernames = FollowersCount.objects.filter(
        follower=request.user.username
    ).values_list('user', flat=True)

    # Optionally include the user's own posts
    followed_usernames = list(followed_usernames)

    # Filter posts by those users
    posts = Post.objects.filter(user__in=followed_usernames).order_by('-created_at')

    data = [
        {
            'id': post.id,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'media': [m.file.url for m in post.media_files.all()],
            'username': post.user,
            'number of likes':post.no_of_likes
        } for post in posts
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    return Response({
        'username': user.username,
        'name': profile.name,
        'email': user.email,
        'bio': profile.bio,
        'profileimg': profile.profileimg.url if profile.profileimg else '',

        'age': profile.age,
        'gender': profile.gender,
        'occupation': profile.occupation,
        'college': profile.college,
        'city': profile.city,
        'state': profile.state,
        'fashion_preferences': profile.fashion_preferences,
        'color_preferences': profile.color_preferences
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profile_posts(request, username):
    posts = Post.objects.filter(user=username).order_by('-created_at')
    data = [
        {
            'id': post.id,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'media': [m.file.url for m in post.media_files.all()],
        } for post in posts
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_saved_posts(request):
    saved = SavedPost.objects.filter(user=request.user).order_by('-saved_at')
    data = [
        {
            'id': entry.post.id,
            'title': entry.post.caption[:30] or 'Untitled',
            'caption': entry.post.caption,
            'media': [m.file.url for m in entry.post.media_files.all()],
        } for entry in saved
    ]
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_for_you(request):
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    # Extract preferences from profile
    preferred_colors = [c.strip().lower() for c in (profile.color_preferences or '').split(',') if c.strip()]
    preferred_items = [i.strip().lower() for i in (profile.fashion_preferences or '').split(',') if i.strip()]

    # Tags from liked posts
    liked_post_ids = LikePost.objects.filter(username=user.username).values_list('post_id', flat=True)
    liked_tags = ApparelTag.objects.filter(post_id__in=liked_post_ids)

    liked_labels = set(tag.label.lower() for tag in liked_tags)
    liked_colors = set(tag.color.lower() for tag in liked_tags if tag.color)
    liked_items = set(tag.item.lower() for tag in liked_tags if tag.item)

    # Unified signals
    all_colors = set(preferred_colors) | liked_colors
    all_items = set(preferred_items) | liked_items
    all_labels = liked_labels

    # Match relevant ApparelTags
    matched_tags = ApparelTag.objects.filter(
        Q(color__in=all_colors) |
        Q(item__in=all_items) |
        Q(label__in=all_labels)
    ).exclude(post__user=user.username).select_related('post')

    post_score = Counter()
    for tag in matched_tags:
        score = 0
        if tag.color and tag.color.lower() in all_colors:
            score += 1
        if tag.item and tag.item.lower() in all_items:
            score += 2
        if tag.label and tag.label.lower() in all_labels:
            score += 1
        post_score[tag.post_id] += score

    # Top personalized post IDs by score
    top_post_ids = [pid for pid, _ in post_score.most_common()]
    top_posts = Post.objects.filter(id__in=top_post_ids)

    personalized_results = []
    for post in top_posts:
        personalized_results.append({
            'id': post.id,
            'username': post.user,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'media': [m.file.url for m in post.media_files.all()],
            'number of likes': post.no_of_likes,
            'score': post_score.get(post.id, 0)
        })

    # Add the rest (non-personalized posts), excluding user & already listed
    all_other_posts = Post.objects.exclude(
        user=user.username
    ).exclude(
        id__in=top_post_ids
    ).order_by('-created_at')

    generic_results = []
    for post in all_other_posts:
        generic_results.append({
            'id': post.id,
            'username': post.user,
            'title': post.caption[:30] or 'Untitled',
            'caption': post.caption,
            'media': [m.file.url for m in post.media_files.all()],
            'number of likes': post.no_of_likes,
            'score': 0
        })

    # Final results = personalized first, then general
    full_results = personalized_results + generic_results

    return Response(full_results)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_search(request):
    query = request.GET.get('q', '').lower().strip()
    query = unidecode(query)  # Handle accented characters

    if not query:
        return Response([])

    # Break into words (e.g., "blue dresses" => ["blue", "dresses"])
    query_parts = query.split()

    # Normalize query by removing plurals (basic heuristic)
    query_parts = [word[:-1] if word.endswith('s') else word for word in query_parts]

    normalized_query = " ".join(query_parts)

    matched_users = User.objects.filter(username__icontains=normalized_query)

    # Get all tags
    matched_tags = ApparelTag.objects.select_related('post', 'image')

    # Prepare known vocab for fuzzy matching
    known_labels = {tag.label.lower() for tag in matched_tags if tag.label}
    known_colors = {tag.color.lower() for tag in matched_tags if tag.color}
    known_items = {tag.item.lower() for tag in matched_tags if tag.item}
    all_known_terms = known_labels | known_colors | known_items

    # Match keywords to known terms using close matches
    def fuzzy_match(word):
        match = difflib.get_close_matches(word, all_known_terms, n=1, cutoff=0.7)
        return match[0] if match else word

    fuzzy_parts = [fuzzy_match(word) for word in query_parts]
    fuzzy_query = " ".join(fuzzy_parts)

    filtered_tags = []
    for tag in matched_tags:
        match_score = 0

        tag_label = (tag.label or '').lower()
        tag_color = (tag.color or '').lower()
        tag_item = (tag.item or '').lower()
        combined = f"{tag_color} {tag_item}"

        for part in fuzzy_parts:
            if part in tag_label:
                match_score += 1
            if part in tag_color:
                match_score += 1
            if part in tag_item:
                match_score += 1
            if part in combined:
                match_score += 2  # compound match

        if match_score > 0:
            filtered_tags.append((tag, match_score))

    # Sort by match score
    filtered_tags.sort(key=lambda x: x[1], reverse=True)

    matched_posts_dict = {}
    for tag, _ in filtered_tags:
        post = tag.post
        if post.id not in matched_posts_dict:
            matched_posts_dict[post.id] = {
                'id': str(post.id),
                'caption': post.caption,
                'media': [m.file.url for m in post.media_files.all()],
                'username': post.user,
                'matched_label': tag.label,
                'color': tag.color,
                'item': tag.item
            }

    results = {
        'users': [
            {'id': f'user-{user.id}', 'username': user.username}
            for user in matched_users
        ],
        'posts': list(matched_posts_dict.values())
    }

    return Response(results)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user.username:
        return Response({'error': 'You are not allowed to delete this post.'}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response({'message': 'Post deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return Response({'error': 'You are not allowed to delete this comment.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': 'Comment deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_recommended_posts(request, post_id):
    try:
        source_post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found.'}, status=404)

    tags = ApparelTag.objects.filter(post=source_post)
    if not tags.exists():
        return Response({'message': 'No apparel tags found for this post.'}, status=200)

    labels = set(tag.label for tag in tags if tag.label)
    items = set(tag.item for tag in tags if tag.item)
    colors = set(tag.color for tag in tags if tag.color)

    similar_tags = ApparelTag.objects.exclude(post=source_post).filter(
        Q(label__in=labels) | Q(item__in=items) | Q(color__in=colors)
    ).select_related('post')

    post_scores = Counter()
    for tag in similar_tags:
        score = 0
        if tag.label in labels:
            score += 2
        if tag.item in items:
            score += 1
        if tag.color in colors:
            score += 1
        post_scores[tag.post_id] += score

    # Sort post IDs by score
    sorted_post_ids = [post_id for post_id, _ in post_scores.most_common(10)]

    # Use in_bulk to fetch posts by ID efficiently
    post_map = Post.objects.in_bulk(sorted_post_ids)

    recommendations = []
    for pid in sorted_post_ids:
        post = post_map.get(pid)
        if not post:
            continue

        matched_tags = ApparelTag.objects.filter(post=post).filter(
            Q(label__in=labels) | Q(item__in=items) | Q(color__in=colors)
        )

        recommendations.append({
            'id': str(post.id),
            'caption': post.caption,
            'media': [media.file.url for media in post.media_files.all()],
            'matched': [
                {
                    'label': tag.label,
                    'item': tag.item,
                    'color': tag.color
                }
                for tag in matched_tags
            ],
            'score': post_scores[pid]
        })

    return Response({
        'source_post': str(source_post.id),
        'matched_labels': list(labels),
        'matched_items': list(items),
        'matched_colors': list(colors),
        'recommendations': recommendations
    })