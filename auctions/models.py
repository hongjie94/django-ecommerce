from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Model for auction list
class Listing(models.Model):
    user = models.CharField(max_length=10)
    title = models.CharField(max_length=65)
    descriptions = models.TextField()
    starting_bid = models.PositiveIntegerField()
    current_bid = models.PositiveIntegerField()
    image_url = models.URLField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=64)
    time_created = models.DateTimeField(auto_now_add=True)


# Model for Bid
class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid_amount = models.PositiveIntegerField()
    time_bade = models.DateTimeField(auto_now_add=True)


# Model for Comment
class Comment(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    comment = models.TextField()
    time_commented = models.DateTimeField(auto_now_add=True)


# Model for Watchlist
class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
    time_added = models.DateTimeField(auto_now_add=True)

