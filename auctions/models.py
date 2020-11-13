from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=112)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="list_creater")
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=1000)
    start_price = models.FloatField(max_length=10)
    img_url = models.URLField(max_length=210)
    watched_by = models.ManyToManyField(User, blank=True, related_name="watching_user")
    def __str__(self):
        return f"{self.title}"
    

class Bid(models.Model):
    bid_price = models.FloatField(max_length=10)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="asBidder")
    time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingbid")
    def __str__(self):
            return f"{self.listing}"

class Comment(models.Model):
    content = models.CharField(max_length=50)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="as_Commenter")
    time = models.DateTimeField(auto_now=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    def __str__(self):
            return f"{self.listing}"

class Category(models.Model):
    name = models.CharField(max_length=20)
    listing = models.ManyToManyField(Listing, blank=True, related_name="of_category")
    parent_category = models.ForeignKey('self', null=True, on_delete=models.CASCADE, 
                                        related_name="p_category")
    def __str__(self):
        return f"{self.name}"
