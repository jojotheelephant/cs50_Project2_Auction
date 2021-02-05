from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Comment, Bid, Watchlist, CATEGORIES
from .forms import AuctionListingForm, CommentForm, BidForm


def index(request):
    '''
    Render active listings
    1. Get all listings filtered by active=True
    2. Pass active listing object to page
    '''
    listings = AuctionListing.objects.filter(active=True).order_by('-date_listed')
    length = len(listings)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "totallistings": length
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    # assign POST to variables
    if request.method == "POST":
        auctionlistingpost = AuctionListingForm(request.POST)
        user = User.objects.get(username=request.user.username)
        if auctionlistingpost.is_valid():
            listing = auctionlistingpost.save(commit=False)
            listing.lister_user = user
            listing.save()
            return render(request, "auctions/createlisting.html", {
                "message": "Listing Posted"
            })
        else: 
            return render(request, "auctions/createlisting.html", {
                "message": auctionlistingpost.errors
            })
    else:
        auctionlistingform = AuctionListingForm()
        return render(request, "auctions/createlisting.html",{
            "auctionlistingform": auctionlistingform
        })

@login_required
def listing(request, listing_id):
    # get current user data
    user = User.objects.get(username=request.user.username)
    # get Listing and Comments from database
    auctionlisting = AuctionListing.objects.get(pk=listing_id)
    listingcomments = Comment.objects.filter(listing=listing_id)
    # check if current user is lister_user or winner_user
    if auctionlisting.lister_user == user:
        userislisteruser = True
    else: 
        userislisteruser = False
    if auctionlisting.winner_user == user:
        useriswinneruser = True
    else: 
        useriswinneruser = False
    # get Watchlist from database
    watchers = Watchlist.objects.filter(listing=listing_id)
    numofwatchers = len(watchers)
    # check if user is watching
    if Watchlist.objects.filter(listing=listing_id).filter(user=user):
        userwatching = True
    else: 
        userwatching = False
    # get Bids from database
    bids = Bid.objects.filter(bid_listing=listing_id).order_by('-value')
    bidscount = len(bids)
    if bids:
        highestbid = bids.first()
    else: 
        highestbid = Bid(value=0)
    # get form models
    bidform = BidForm()
    commentform = CommentForm()
    '''
    # if POST request received
    1. check if POST method received
        1. check if watchlist (validation is in render page)
            1a. take user and listing and add to watchlist
            1b. re-render page
        2. check if unwatchlist (validation is in render page)
            2a. take user and listing and remove from watchlist
            2b. re-render page
        3. check if bid (validation is in render page)
            3a. check if bid value is greater than current price
            3b. save to bid database
            3c. re-render page
        4. check if comments
            4a. save comment to database
            4b. re-render page
        5. check if closelisting (validation is in render page)
            5a. save to database
    '''

    # check if request.method == POST and listing is active
    if request.method == "POST":
        # if button == unwatchlist
        if request.POST.get("button") == "unwatchlist":
            user.watchlist.filter(listing=auctionlisting).delete()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        # if button == watchlist
        elif request.POST.get("button") == "watchlist":
            addtowatchlist = Watchlist(user=user, listing=auctionlisting)
            addtowatchlist.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        # if button == submitbid
        elif request.POST.get("button") == "Submit Bid":
            value = float(request.POST.get("value"))
            # if value of bid is less than current prices, reload page with warning message.
            if value < highestbid.value or value < auctionlisting.price: 
                return render(request, "auctions/listing.html",{
                    "listings": auctionlisting,
                    "highestbid": highestbid,
                    "bids": bids,
                    "bidscount": bidscount,
                    "bidform": bidform, 
                    "commentform": commentform,
                    "comments": listingcomments,
                    "numofwatchers": numofwatchers,
                    "userwatching": userwatching,
                    "userislisteruser": userislisteruser, 
                    "useriswinneruser": useriswinneruser,
                    "bidmessage": "Your bid must be greater than current price."
                })
            submitbid = Bid(bid_listing=auctionlisting, user=user, value=value)
            submitbid.save()
            auctionlisting.price = value
            auctionlisting.winner_user = user
            auctionlisting.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        # if button == "Post Comment"
        elif request.POST.get("button") == "Post Comment":
            comment = request.POST.get("comment")
            addtocomment = Comment(user=user, comment=comment, listing=auctionlisting)
            addtocomment.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        # if button == "closelisting"
        elif request.POST.get("button") == "closelisting":
            auctionlisting.active = False
            auctionlisting.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
        # if button == "openlisting"
        elif request.POST.get("button") == "openlisting":
            auctionlisting.active = True
            auctionlisting.save()
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
    else:
        return render(request, "auctions/listing.html",{
            "listings": auctionlisting,
            "highestbid": highestbid,
            "bids": bids,
            "bidscount": bidscount,
            "bidform": bidform, 
            "commentform": commentform,
            "comments": listingcomments,
            "numofwatchers": numofwatchers,
            "userwatching": userwatching,
            "userislisteruser": userislisteruser, 
            "useriswinneruser": useriswinneruser
        })

@login_required
def watchlist(request):
    user = User.objects.get(username=request.user.username)
    mywatchlist = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": mywatchlist
    })

@login_required
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": CATEGORIES
    })

@login_required
def category(request, category):
    categorylistings = AuctionListing.objects.filter(category=category[0])
    categorydict = dict(CATEGORIES)[category]
    return render(request, "auctions/categories.html", {
        "categorylistings": categorylistings,
        "categorydict": categorydict
    })