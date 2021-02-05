from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, AuctionListing, Comment, Bid, Watchlist

# class view
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id","product_name", "price","category", "lister_user","date_listed", "active" )

class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_listing", "value", "user", "date_bid")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", "user", "comment", "date_posted")

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(AuctionListing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)



