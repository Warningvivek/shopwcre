from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, ProfileForm, FeedbackForm, CollectionForm
from .models import Collection, User, Feedback
from django.core.paginator import Paginator

def home(request):
    creators = User.objects.filter(role=User.CREATOR).order_by('-date_joined')[:4]
    collections = Collection.objects.all().order_by('-created_at')[:8]
    return render(request, 'aggregator/home.html', {
        'collections': collections,
        'creators': creators
    })

def creator_list(request):
    creators = User.objects.filter(role=User.CREATOR).order_by('-date_joined')
    return render(request, 'aggregator/creator_list.html', {'creators': creators})

def creator_detail(request, username):
    creator = get_object_or_404(User, username=username, role=User.CREATOR)
    collections = creator.collections.all().order_by('-created_at')
    return render(request, 'aggregator/creator_detail.html', {
        'creator': creator,
        'collections': collections
    })

def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    is_liked = False
    if request.user.is_authenticated:
        is_liked = collection.likes.filter(id=request.user.id).exists()
    return render(request, 'aggregator/collection_detail.html', {
        'collection': collection,
        'is_liked': is_liked
    })

@login_required
def like_collection(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        collection_id = request.POST.get('collection_id')
        collection = get_object_or_404(Collection, id=collection_id)
        
        if collection.likes.filter(id=request.user.id).exists():
            collection.likes.remove(request.user)
            liked = False
        else:
            collection.likes.add(request.user)
            liked = True
        
        return JsonResponse({'liked': liked, 'total_likes': collection.likes.count()})
    return JsonResponse({}, status=400)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'aggregator/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'aggregator/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    collections = None
    if request.user.role == User.CREATOR:
        collections = request.user.collections.all().order_by('-created_at')
    
    return render(request, 'aggregator/profile.html', {
        'form': form,
        'collections': collections
    })

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('home')
    else:
        initial = {'email': request.user.email} if request.user.is_authenticated else {}
        form = FeedbackForm(initial=initial)
    
    return render(request, 'aggregator/feedback.html', {'form': form})

@login_required
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    feedbacks = Feedback.objects.filter(responded=False).order_by('-created_at')
    users = User.objects.all().order_by('-date_joined')
    
    return render(request, 'aggregator/dashboard.html', {
        'feedbacks': feedbacks,
        'users': users
    })

@login_required
def add_collection(request):
    if request.user.role != User.CREATOR:
        messages.error(request, "Only creators can add collections.")
        return redirect('home')
    
    if request.method == 'POST':
        form = CollectionForm(request.POST, request.FILES, creator=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Collection added successfully!')
            return redirect('profile')
    else:
        form = CollectionForm(creator=request.user)
    
    return render(request, 'aggregator/add_collection.html', {'form': form})



from rest_framework import generics
from .serializers import UserSerializer, CollectionSerializer, FeedbackSerializer

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class FeedbackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer