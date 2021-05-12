from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from pip._vendor.distlib.compat import raw_input
from .models import *


# Homepage
def index(request):
    """

    :param request:
    :return:
    """
    # Get all exist listings.
    listings = Listing.objects.all()
    # Show all listings in index/home page
    return render(request, "auctions/index.html", {"listings": listings})


# Login page
def login_view(request):
    """

    :param request:
    :return:
    """

    # Check if method is POST
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


# Logout and takes user to index/home page
def logout_view(request):
    """

    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register page
def register(request):
    """

    :param request:
    :return:
    """
    # Check if method is POST
    if request.method == "POST":

        # Get username
        username = request.POST["username"]
        # Get email
        email = request.POST["email"]

        # Ensure password matches confirmation and username validity
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if username == "":
            return render(request, "auctions/register.html", {
                "message": "Must provide a username."
            })

        if password == "":
            return render(request, "auctions/register.html", {
                "message": "Must provide a password."
            })

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



def active_listings(request, listing_id):
    """

    :param request:
    :param listing_id:
    :return:
    """
    # Check if method is GET
    if request.method == "GET":

        listing = Listing.objects.get(pk=listing_id)

        exist_comment = Comment.objects.filter(listingid=listing_id)

        highest_bid = Bid.objects.filter(listingid=listing_id)

        items = []

        for i in highest_bid:
            items.append(Bid.objects.filter(listingid=i.listingid))

        # Return to active listing page displaying listing and comments and bid
        try:
            return render(request, "auctions/active_listings.html", {
                "listings": listing,
                "bid": items,
                "comments": exist_comment
            })

        # If not exist
        except listing.image_url == "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603406015459&di=06f631ced7a0f89f5ed83f49bd313e51&imgtype=0&src=http%3A%2F%2Fku.90sjimg.com%2Felement_origin_min_pic%2F17%2F07%2F28%2F37d6a9a47547ddefe2050516bdda5cd1.jpg":
            return render(request, "auctions/index.html", {
                "listings": listing,
                "winner": items,
                "message_bb": "yeah hu",
                "comments": exist_comment
            })
    else:
        return redirect('active_listings')


# Watchlist page user able to view all watchlist
@login_required(login_url='/login')
def watchlist(request):
    # Check if method is GET
    if request.method == "GET":

        # Get username
        current_user = request.user.username

        # Query watchlist from db who's username is current user
        watchlist = Watchlist.objects.filter(user=current_user)

        # Create an empty list
        items = []

        # Iterate watchlist for i/listings and append to empty list
        for i in watchlist:
            items.append(Listing.objects.filter(id=i.listingid))

        count_watchlist = len(watchlist)

        # Return watchlist page with all appended listings
        return render(request, "auctions/watchlist.html", {
            "watchlist": items,
            "count": count_watchlist
        })


# Add Items to watchlist
@login_required(login_url='/login')
def add_watchlist(request, listingid):
    # Check if method is GET
    if request.method == "GET":

        highest_bid = Bid.objects.filter(listingid=listingid)
        items = []

        for i in highest_bid:
            items.append(Bid.objects.filter(listingid=i.listingid))
        current_user = request.user.username

        all_comments = Comment.objects.filter(listingid=listingid)

        # Get listing and watchlist for current user
        listing = Listing.objects.get(pk=listingid)
        watchlist = Watchlist.objects.filter(listingid=listingid)

        if Watchlist.objects.filter(listingid=listingid).exists():

            return render(request, "auctions/active_listings.html", {
                "listings": listing,
                "comments": all_comments,
                "bid": items,
                "message_exist_wl": " "
            })
        else:
            # Add watchlist to db where user is current user and listings from current user
            add_watchlist = Watchlist.objects.create(
                user=current_user,
                listingid=listing.id)
            add_watchlist.save()

            # Return active listing page notice user watchlist is added
            all_comments = Comment.objects.filter(listingid=listingid)
            return render(request, "auctions/active_listings.html", {
                "listings": listing,
                "comments": all_comments,
                "bid": items,
                "message_wl": " "
            })

    # Return to index page
    else:
        redirect('index')


# Remove Items from watchlist
@login_required(login_url='/login')
def remove_watchlist(request, listingid):
    # Check if method is GET
    if request.method == "GET":

        # Remove item form watchlist.
        remove_watchlist = Watchlist.objects.filter(listingid=listingid)
        remove_watchlist.delete()

        # Iterate watchlist and get all the exist listings and get number of watchlist
        watchlist = Watchlist.objects.filter(user=request.user.username)
        count_watchlist = len(watchlist)
        items = []
        for i in watchlist:
            items.append(Listing.objects.filter(id=i.listingid))

        # Return watchlist page , notice user that item is remove
        return render(request, "auctions/watchlist.html", {
            "watchlist": items,
            "count": count_watchlist,
            "message": "Item successfully remove from Watchlist."
        })
    else:
        redirect('index')


# Make comments to listings
@login_required(login_url='/login')
def comment(request, listingid):
    # Check if method is POST
    if request.method == "POST":

        # Get comments, user, listing
        user_comments = request.POST["comment"]
        current_user = request.user.username
        listing = Listing.objects.get(pk=listingid)

        # Save to database
        add_comment = Comment.objects.create(
            user=current_user,
            listingid=listing.id,
            comment=user_comments)
        add_comment.save()

        # Return to active listing page displaying comments and listings
        listing = Listing.objects.get(pk=listingid)
        all_comments = Comment.objects.filter(listingid=listingid)
        return render(request, "auctions/active_listings.html", {
            "listings": listing,
            "comments": all_comments,
            "message_c": "Comment successfully added."
        })

        # If method is GET return to active listing page displaying listings and comments
    else:
        listing = Listing.objects.get(pk=listingid)
        all_comments = Comment.objects.filter(listingid=listingid)
        return render(request, "auctions/active_listings.html", {
            "listings": listing,
            "comments": all_comments
        })


# Create new listing (login required)
@login_required(login_url='/login')
def create_listing(request):
    """

    :param request:
    :return:
    """
    # Check if method is POST
    if request.method == "POST":

        # Get all info form user
        title = request.POST["title"]
        descriptions = request.POST["descriptions"]
        starting_bid = int(request.POST["starting_bid"])
        current_bid = starting_bid
        category = request.POST["category"]
        user = request.user.username

        # Set a default image for user if there is no image
        if request.POST.get('image_url'):
            image_url = request.POST.get('image_url')
        else:
            image_url = "https://www.gooutdoors.co.uk/images/20200228123908/ap/resizeandpad:478:478/no_image_available.gif&qlt=80"

        # Ensure starting bid amount is valid
        if request.POST["starting_bid"] == "":
            return render(request, "auctions/create_listing.html", {
                "message": "Invalid Starting Bid!"
            })

        # Attempt to create new listing
        try:
            new_listing = Listing.objects.create(
                user=user,
                title=title,
                descriptions=descriptions,
                starting_bid=starting_bid,
                current_bid=current_bid,
                image_url=image_url,
                category=category
            )
            new_listing.save()
        except:
            return render(request, "auctions/create_listing.html", {
                "message": "listings already exist."
            })

        # Get all latest listings and listing count, return to my listing page  
        listings = Listing.objects.filter(user=request.user.username)
        count_listings = len(listings)
        return render(request, "auctions/my_listings.html",
                      {"listings": listings, 
                       "count": count_listings,
                       "message": "Listing was added successfully"})

    else:
        return render(request, "auctions/create_listing.html")


# If User is login user is able to view their posted listings
@login_required(login_url='/login')
def my_listings(request):
    """

    :param request:
    :return:
    """

    # Check if method is POST
    if request.method == "GET":
        # Get the listings and return to my listing page
        listings = Listing.objects.filter(user=request.user.username)
        count_listings = len(listings)
        return render(request, "auctions/my_listings.html", {
            "listings": listings,
            "count": count_listings
        })


# Add bid amount to items
@login_required(login_url='/login')
def bid(request, listing_id):
    # Query listing from db
    listing = Listing.objects.get(id=listing_id)

    # Get current_bid from listing
    current_bid = listing.current_bid

    # Get starting_bid form listing
    starting_bid = listing.starting_bid

    highest_bid = Bid.objects.filter(listingid=listing_id)

    items = []
    for i in highest_bid:
        items.append(Bid.objects.filter(listingid=i.listingid))

    # Query Comment from db
    exist_comment = Comment.objects.filter(listingid=listing_id)

    if request.method == "POST":

        # Get user bid amount
        ub = request.POST["bid"]
        if ub.isdigit():
            user_bid = int(ub)

        # If bid is closed display sold image and bid summit button disable
        elif listing.image_url == "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603406015459&di=06f631ced7a0f89f5ed83f49bd313e51&imgtype=0&src=http%3A%2F%2Fku.90sjimg.com%2Felement_origin_min_pic%2F17%2F07%2F28%2F37d6a9a47547ddefe2050516bdda5cd1.jpg":
            user_bid = raw_input(None)

        # Ensure user input is valid
        else:
            user_bid = int(raw_input(ub))

        # Ensure user bid amount greater than starting bid and listing is active
        if user_bid > current_bid and not listing.image_url == "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603406015459&di=06f631ced7a0f89f5ed83f49bd313e51&imgtype=0&src=http%3A%2F%2Fku.90sjimg.com%2Felement_origin_min_pic%2F17%2F07%2F28%2F37d6a9a47547ddefe2050516bdda5cd1.jpg":

            # Get current bid listing
            exist_listing = Listing.objects.get(id=listing_id)

            # Set current bid in listing to user bid
            exist_listing.current_bid = user_bid

            # Replace current bid to user bid who is higher than current bid
            exist_listing.save()

            # Delete the previous bid from db
            exist_bid = Bid.objects.filter(listingid=listing_id)
            exist_bid.delete()

            # Add new bid to db
            new_bid = Bid()
            new_bid.user = request.user.username
            new_bid.title = exist_listing.title
            new_bid.listingid = listing_id
            new_bid.bid_amount = user_bid
            new_bid.save()

            # Return to active listing page notice user bid is added
            return render(request, "auctions/active_listings.html", {
                "listings": exist_listing,
                "comments": exist_comment,
                "bid": items,
                "message_b": "Your Bid is added."
            })

            # If listing is closed send winner message
        elif listing.image_url == "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603406015459&di=06f631ced7a0f89f5ed83f49bd313e51&imgtype=0&src=http%3A%2F%2Fku.90sjimg.com%2Felement_origin_min_pic%2F17%2F07%2F28%2F37d6a9a47547ddefe2050516bdda5cd1.jpg":

            exist_listing = Listing.objects.get(id=listing_id)

            # Return current page and update bid amount on the page
            return render(request, "auctions/active_listings.html", {
                "listings": exist_listing,
                "comments": exist_comment,
                "bid": items,
                "message_winner": "Item is Sold! Winner "
            })

            # Return active listings page  notice user bid have to have higher then current amount
        else:
            exist_listing = Listing.objects.get(id=listing_id)
            return render(request, "auctions/active_listings.html", {
                "listings": exist_listing,
                "comments": exist_comment,
                "bid": items,
                "message_b": " Your Bid should be higher than Current bid!",
            })

    else:
        redirect('active_listings')


# Close a listing/ bid
@login_required(login_url='/login')
def close_bid(request, listing_id):

    # If bid close change the item image
    if request.user.username:
        image = "https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1603406015459&di=06f631ced7a0f89f5ed83f49bd313e51&imgtype=0&src=http%3A%2F%2Fku.90sjimg.com%2Felement_origin_min_pic%2F17%2F07%2F28%2F37d6a9a47547ddefe2050516bdda5cd1.jpg"
        exist_listing = Listing.objects.get(pk=listing_id)
        exist_listing.image_url = image
        exist_listing.save()

        listings = Listing.objects.filter(user=request.user.username)
        count_listings = len(listings)
        return render(request, "auctions/my_listings.html", {
            "listings": listings,
            "count": count_listings
        })


# Close a listing/ bid
@login_required(login_url='/login')
def deleted_listing(request, listing_id):

    # Get query form db and deleted the listing
    if request.user.username:
        exist_listing = Listing.objects.get(pk=listing_id)
        exist_listing.delete()

        # Count number of listings
        listings = Listing.objects.filter(user=request.user.username)
        count_listings = len(listings)
        return render(request, "auctions/my_listings.html", {
            "listings": listings,
            "count": count_listings
        })


# Categories Fashion page
def fashion(request):
    # Get all exist listings
    fashion = Listing.objects.filter(category="Fashion")

    # Show all listings in Fashion page
    return render(request, "auctions/fashion.html", {"listings": fashion})


# Categories Toys page
def toy(request):
    # Get all exist listings
    toys = Listing.objects.filter(category="Toys")

    # Show all listings in Toys page 
    return render(request, "auctions/toy.html", {"listings": toys})


# Categories Electronic page
def electronic(request):
    # Get all exist listings
    electronic = Listing.objects.filter(category="Electronic")

    # Show all listings in Electronic page 
    return render(request, "auctions/electronic.html", {"listings": electronic})


# Categories Home page    
def home(request):
    # Get all exist listings
    home = Listing.objects.filter(category="Home")

    # Show all listings in Fashion page 
    return render(request, "auctions/home.html", {"listings": home})


# Categories Everything page 
def everything(request):
    # Get all exist listings
    everything = Listing.objects.filter(category="Everything Else")

    # Show all listings in Everything page 
    return render(request, "auctions/everything.html", {"listings": everything})
