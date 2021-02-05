from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey, ManyToManyField


# for default image if link to product image not provided
def default_img():
    return "https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.mcssl.com%2Fcontent%2F262147%2Fproducts-corrugated-stock-boxes-shipping-kraft-shorr-packaging_0.jpg&f=1&nofb=1"
# format time
def date_format(date):
    return date.strftime("%m/%d/%Y %H:%M")
# categories
CATEGORIES = (
    ('1', 'Devil Fruit'),
    ('2', 'Weapon'),
    ('3', 'Transportation'),
    ('4', 'Food'),
    ('5', 'Rare Item'),
    ('6', 'Crewmate'),
)

# MODELS
class User(AbstractUser):
    pass

    def __str__(self): 
        return self.get_full_name()

class AuctionListing(models.Model):
    product_name = models.CharField(max_length=60, blank=False)
    price        = models.DecimalField(max_digits=8, decimal_places=2)
    description  = models.CharField(max_length=1000, blank=False)
    active       = models.BooleanField(default=True)
    lister_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rn_lister")
    winner_user  = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="rn_winner")
    category     = models.CharField(max_length=2, choices=CATEGORIES, default=CATEGORIES[0])
    date_listed  = models.DateTimeField(auto_now_add=True)
    image        = models.URLField(max_length=300, default=default_img)

    def __str__(self):
        return f"{self.id}-{self.product_name}: ${self.price} ({date_format(self.date_listed)})"

# class Category(models.Model):
#     category_name = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="category")

#     def __str__(self):
#         return f"{self.category_name}"

class Comment(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    comment      = models.CharField(max_length=250)
    date_posted  = models.DateTimeField(auto_now_add=True)
    listing      = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} posted: '{self.comment}' ({date_format(self.date_posted)})"

class Bid(models.Model):
    value        = models.DecimalField(max_digits=8, decimal_places=2)
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_listing  = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid")
    date_bid     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.bid_listing.product_name} @ ${self.value} - {self.user} ({date_format(self.date_bid)})"

class Watchlist(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing      = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is watching {self.listing}"