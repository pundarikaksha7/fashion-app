from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

User = get_user_model()



class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}"

# Create your models here.
# models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    firebase_uid = models.CharField(max_length=128, unique=True)  

    # Existing fields
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)

    # New fields
    name = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    fashion_preferences = models.TextField(blank=True)
    color_preferences = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=100)
    # image = models.FileField(upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    is_apparel = models.BooleanField(default=False)  # flag post relevance
    def __str__(self):
        return self.user
    @property
    def profile_image(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user_obj = User.objects.get(username=self.user)
            # Use profile_set.first() since the relationship is a ForeignKey.
            profile = user_obj.profile_set.first()
            if profile:
                return profile.profileimg.url
            else:
                return '/media/profile_images/blank-profile-picture.png'
        except User.DoesNotExist:
            return '/media/profile_images/blank-profile-picture.png'
    @property
    def saved_by(self):
        return [saved_post.user for saved_post in self.saved_by.all()]

class PostMedia(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='post_media')
    is_image = models.BooleanField(default=True)  # True for image, False for video
    
class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-saved_at']
    def __str__(self):
        return f"{self.user.username} saved post {self.post.id}"
    
class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

# New Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.id}"

    @property
    def profile_image(self):
        try:
            profile = self.user.profile_set.first()
            if profile and profile.profileimg:
                return profile.profileimg.url
        except AttributeError:
            pass  # If profile does not exist or has no image

        return '/media/profile_images/blank-profile-picture.png'
    
# # Apparel Classifier model
# class ApparelTag(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     image = models.ForeignKey(PostMedia, on_delete=models.CASCADE)
#     label = models.CharField(max_length=50)
#     confidence = models.FloatField()

class ApparelTag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ForeignKey(PostMedia, on_delete=models.CASCADE)
    
    label = models.CharField(max_length=50)  # e.g., 't-shirt', 'jeans'
    confidence = models.FloatField()

    # New fields
    color = models.CharField(max_length=30, blank=True, null=True)
    item = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.label} ({self.color}, {self.pattern}, {self.style})"
