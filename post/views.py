from django.shortcuts import render
from .models import Post, Comment
from users.models import Profile
from django.views.generic import (
    ListView,
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import *
from rest_framework import viewsets
from rest_framework.decorators import detail_route, action
from .serializers import PostSerialize, CommentSerialize, ProfileSerialize
from django.http import HttpResponseRedirect
from rest_framework.response import Response



class ShowPostView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'post'
    ordering = ['-date']

    def get_context_data(self, **kwards):
        ctx = super(ShowPostView, self).get_context_data(**kwards)
        ctx['title'] = 'Главная страница блога'
        return ctx
def show_post(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        reply_form = CommentReplyForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            rating = request.POST.get('rating')
            comment = Comment.objects.create(post=post,user=request.user, content=content, rating=rating)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
        
        if reply_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post,user=request.user, content=content,reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    
    else:
        comment_form = CommentForm()
        reply_form = CommentReplyForm()

    return render(request,'post/post_detail.html',
                  {'post': post,'comments': comments,'comment_form': comment_form,'reply_form': reply_form })



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

    
# class PostView(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerialize
    
    
#     @detail_route(url_name='comment')
#     def comment(self, request, pk=None, comment_id=None):
#         post = Post.objects.get(id=pk)
#         # queryset = Comment.objects.filter(book__pk=pk)
#         queryset = Comment.objects.filter(post=post, reply=None).order_by('-id')
#         serializer = CommentSerialize(queryset,
#                         context={'request':request},
#                         many=True)
#         return Response(serializer.data)

class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerialize
    
    @detail_route(methods=['get'])
    def comment(self, request, pk=None, comment_id=None):

        post = Post.objects.get(id=pk)
        queryset = Comment.objects.filter(post=post, reply=None).order_by('-id')
        serializer = CommentSerialize(queryset,
                        context={'request':request},
                        many=True)
        return Response(serializer.data)
    
class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerialize
    
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerialize
    