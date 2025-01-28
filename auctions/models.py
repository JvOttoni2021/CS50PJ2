from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    def add_to_watchlist(self, listing):
        if listing.user == self:
            return "Cannot add your own listing to watchlist"
        
        already_in_watchlist = WatchList.objects.filter(user=self, listing=listing, active=True).exists()
        if already_in_watchlist:
            return "The listing is already in your watchlist"
        
        watchlist = WatchList(user=self, listing=listing)
        watchlist.save()
        return "Listing added to watchlist"


class Entity(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateField(default=datetime.now)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True


class Category(Entity):
    name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.name


class Listing(Entity):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)
    starting_bid = models.FloatField(null=False)
    image_url = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='listings')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='listings', null=True)
    is_open = models.BooleanField(null=False, default=True)

    def __str__(self):
        return f"{self.title} - {self.starting_bid}"
    
    def add_comment(self, comment, user):
        new_comment = Comment(user=user, comment_content=comment, listing=self)
        new_comment.save()
    
    def get_highest_value(self):
        bid_list = self.bids
        if not bid_list.exists():
            return self.starting_bid
        
        return sorted(bid_list, key=lambda bid: bid.bid_value, reverse=True)[0]
    
    def is_valid(self):
        if self.description == "":
            return False
        
        if self.title == "":
            return False
        
        if not float(self.starting_bid) > 0:
            return False
        
        return True


class Bid(Entity):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="bids")
    bid_value = models.FloatField(null=False)


class WatchList(Entity):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="watchlist")


class Comment(Entity):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="comments")
    comment_content = models.CharField(max_length=255, null=False)
    