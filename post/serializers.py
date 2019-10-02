from rest_framework import serializers
from .models import Post,Comment
from users.models import Profile

class PostSerialize(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','title', 'text', 'img','date', 'author')
        
class CommentSerialize(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content', 'timestamp', 'post','user_id','reply')
        
class ProfileSerialize(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','img','user')