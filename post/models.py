from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    img = models.ImageField(default='default_post.png', upload_to='post_images')
    date = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Post'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 512 or image.width >512:
            resize = (512,512)
            image.thumbnail(resize)
            image.save(self.img.path)
    
class Comment(models.Model):
    comment = models.CharField(max_length=100)
    rating = models.SmallIntegerField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Comment'
        
class Reply(models.Model):
    reply = models.CharField(max_length=100)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Reply'