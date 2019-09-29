from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('post', views.PostView)

urlpatterns = [
    path('', views.ShowPostView.as_view(), name='post-home'),
    path('api/', include(router.urls), name='post-api'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='post-delete'),
    path('post/add/', views.CreatePostView.as_view(), name='post-add'),
    
    
    # path('post/<int:pk>/', views.ShowCommentView.as_view(), name='show-comment'),
]
