from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    CREATOR = 'creator'
    BUYER = 'buyer'
    ROLE_CHOICES = [
        (CREATOR, 'Creator'),
        (BUYER, 'Buyer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    class Meta:
        app_label = 'aggregator'

    def __str__(self):
        return self.username

class Collection(models.Model):
    CATEGORY_CHOICES = [
        ('MEN', 'Men'),
        ('WOMEN', 'Women'),
        ('UNISEX', 'Unisex'),
    ]
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='collections')
    source_url = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_collections', blank=True)

    def __str__(self):
        return self.title

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback from {self.email}"