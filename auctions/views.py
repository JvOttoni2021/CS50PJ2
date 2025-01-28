from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment
from .forms_constructors import NewListingForm
import traceback


def index(request, title=""):
    user = request.user
    listings = Listing.objects.filter(is_open=True)
    if title == "Watchlist" and user.is_authenticated:
        watchlists = user.watchlist.all()
        listings = [item.listing for item in watchlists]
        title = title.capitalize()
    if title == "My Listings" and user.is_authenticated:
        listings = user.listings.all()
    else:
        title="Active Listings"

    return render(request, "auctions/index.html", {
        "title": title,
        "listings": listings
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

@login_required(login_url="login")
def show_listing(request, listing_id):
    user = request.user
    watchlist_message, comment_message, bid_message = "", "", ""
    try:
        listing_id = int(listing_id)
        listing = Listing.objects.filter(id=listing_id).first()

        if request.method == "POST":
            action = request.POST.get("action")

            if action == "Watchlist":
                watchlist_message = user.add_to_watchlist(listing)

            elif action == "Add Comment":
                comment = request.POST.get("new_comment")
                comment_message = listing.add_comment(comment, user)

            elif action == "Place Bid":
                bid_value = request.POST.get("new_bid_value")
                bid_message = listing.add_bid(bid_value, user)

            elif action == "Close":
                listing.close()
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist_message": watchlist_message,
            "comment_message": comment_message,
            "bid_message": bid_message
        })
    except:
        print(traceback.format_exc())
        return render(request, "auctions/listing.html", {
            "listing": None
        })


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


def create_listing(request):
    user = request.user
    if request.method == "POST":
        form = NewListingForm(request.POST)
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        category = Category.objects.filter(id=request.POST["category"]).first()
        listing = Listing(title=title, 
                          description=description, 
                          starting_bid=starting_bid, 
                          image_url=image_url,
                          category=category,
                          user=user,
                          is_open=True)
        
        if listing.is_valid():
            listing.save()
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })

    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })