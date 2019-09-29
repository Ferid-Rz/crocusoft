from django import forms
from .models import Post, Comment



class PostImage(forms.ModelForm):
    def __init__(self, *args, **kwards):
        super(PostImage, self).__init__(*args, **kwards)
        # self.fields['title'].label = "Title for post"
        self.fields['img'].label = "Post picture"
    class Meta:
        model = Post
        fields = ['img']

class ShowComment(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ['comment']