from django.urls import path
from . import views
from .views import (UserList, UserDetail, CollectionList, CollectionDetail, FeedbackList, FeedbackDetail)
urlpatterns = [
    path('', views.home, name='home'),
    path('creators/', views.creator_list, name='creator_list'),
    path('creators/<str:username>/', views.creator_detail, name='creator_detail'),
    path('collections/add/', views.add_collection, name='add_collection'),
    path('collections/<int:pk>/', views.collection_detail, name='collection_detail'),
    path('like-collection/', views.like_collection, name='like_collection'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('feedback/', views.feedback, name='feedback'),
    path('dashboard/', views.dashboard, name='dashboard'),

     path('api/users/', UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('api/collections/', CollectionList.as_view(), name='collection-list'),
    path('api/collections/<int:pk>/', CollectionDetail.as_view(), name='collection-detail'),
    path('api/feedback/', FeedbackList.as_view(), name='feedback-list'),
    path('api/feedback/<int:pk>/', FeedbackDetail.as_view(), name='feedback-detail'),
]