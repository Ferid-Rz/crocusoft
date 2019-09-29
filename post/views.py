from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostImage, ShowComment
from rest_framework import viewsets
from .serializers import PostSerialize


class ShowPostView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'post'
    ordering = ['-date']

    def get_context_data(self, **kwards):
        ctx = super(ShowPostView, self).get_context_data(**kwards)
        ctx['title'] = 'Главная страница блога'
        return ctx

class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwards):
        ctx = super(PostDetailView, self).get_context_data(**kwards)
        ctx['title'] = Post.objects.filter(pk=self.kwargs['pk']).first()
        return ctx

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text','img']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.img = self.request.FILES['img']

        return super().form_valid(form)

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text','img']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.img = self.request.FILES['img']
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView ):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def contacts(request):
    return render(request, 'post/contacts.html')

# now starting comments 
class ShowCommentView(ListView):
    model = Comment
    template_name = 'post/post_detail.html'
    context_object_name = 'comment'
    # ordering = ['-date']

    def get_context_data(self, **kwards):
        ctx = super(ShowPostView, self).get_context_data(**kwards)
        ctx['title'] = 'Our Post'
        return ctx

class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['comment']
    
    def form_valid(self, form):
        comment = ShowComment(instance=self.request.user.profile)
        data = {
        'comment' : comment
        }
        return render(self.request, 'post/post_detail.html', data)
    

    
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerialize
    