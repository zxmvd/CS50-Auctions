from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import Textarea, ModelForm
from django.contrib import messages
import datetime

from .models import User, Listing, Bid, Comment, Category

class CreateListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}),label="Title for the new listing")
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}), label="Disciption for The listing")
    start_price = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-control'}),label="Bid Start Price")
    img_url = forms.URLField(widget=forms.URLInput(attrs={'class' : 'form-control'}), label="image url")
    category = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class' : 'form-control'}), queryset=Category.objects.all())

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
    return render(request, "auctions/login.html")
    # return HttpResponseRedirect(reverse("index"))


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

def index(request):
    listings = Listing.objects.filter(is_active=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings, "active" : True, "all_categories" : all_categories
    })

def all_listings(request):
    listings = Listing.objects.all()
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings, "all": True, "all_categories" : all_categories
    })

@login_required
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            seller = request.user
            description = form.cleaned_data["description"]
            start_price = form.cleaned_data["start_price"]
            img_url = form.cleaned_data["img_url"]
            selected_categories= form.cleaned_data["category"]

            l = Listing(title=title, seller=seller, description=description, 
            start_price=start_price, img_url=img_url)
            l.save()
            for i in selected_categories:
                l.of_category.add(i)
                # this works well too:):pretty much same way
                # i.listing.add(l)
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create.html", {
        "create_listing_form" : CreateListingForm()
    })




@login_required
def my_listings(request):
    user = request.user
    my_listings = user.list_creater.all()
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {"listings" : my_listings, "my": True, "all_categories" : all_categories})

@login_required
def close_listing(request, list_title, listing_id):
    listing = Listing.objects.get(title=list_title, id=listing_id)
    winning_bid = listing.listingbid.last()
    listing.is_active = False
    listing.save()
    messages.info(request, 'Successfully closed the listing!')
    return HttpResponseRedirect(reverse("product", args=(listing.id,)))

@login_required
def watch_list(request):
    user = request.user
    listings = user.watching_user.all()
    return render(request, "auctions/index.html", 
    {"listings" : listings, "watch": True})

@login_required
def addwatch(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    current_user = request.user
    listing.watched_by.add(current_user)
    messages.info(request, 'Successfully added to your watchlist!')
    return HttpResponseRedirect(reverse("product", args=(listing.id,)))

@login_required
def stopwatch(request, list_id):
    listing = Listing.objects.get(id=list_id)
    current_user = request.user
    listing.watched_by.remove(current_user)
    messages.info(request, 'Successfully removed from your watchlist!')
    return HttpResponseRedirect(reverse("product", args=(listing.id,)))

@login_required
def won_listings(request):
    won_listing = []
    won_price = []
    closed_listings = Listing.objects.filter(is_active=False)
    for listing in closed_listings:
        if listing.listingbid is not None and listing.listingbid.last().bidder == request.user:
            wonbidprice = listing.listingbid.last().bid_price
            won_listing.append(listing)
            won_price.append(wonbidprice)
    return render(request, "auctions/won_listings.html", {"won_listings" : won_listing, 
                "won_price": won_price})

def product(request, product_id):
    productDetail = Listing.objects.get(pk=product_id)
    bids = productDetail.listingbid.all()
    winning_bid = None
    owner = False
    is_watching = False
    comments = productDetail.comments.all()
    all_categories = Category.objects.all()
    categories = productDetail.of_category.all()
    if request.user.is_authenticated:
        if productDetail in request.user.watching_user.all():
            is_watching = True
        else:
            is_watching = False
    if productDetail.seller == request.user:
        owner = True
    if productDetail.is_active == False:
        winning_bid = productDetail.listingbid.last()
    return render(request, "auctions/product.html", {"listing" : productDetail, "bids" :bids, 
    "winning_bid": winning_bid, "owner": owner, "categories": categories, "comments":comments, 
    "all_categories":all_categories, "is_watching":is_watching})

def categories(request):
    all_categories=Category.objects.all()
    all_p_category = Category.objects.filter(parent_category=None)

    return render(request, "auctions/categories.html", {"all_categories" : all_categories})

def show_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(of_category=category)
    all_categories = Category.objects.all()
    if category.parent_category == None:
        s_categories = category.p_category.all()
        for i in s_categories:
            listings_i = Listing.objects.filter(of_category=i)
            # Use union operator for queryset | to take union of two queryset. 
            # If both queryset belongs to same model / single model than it is possible to 
            # combine querysets by using union operator.
            listings = listings.union(listings_i)
            # listings = listings | listings_i

            # distinct() removes duplicated data in queryset
    return render(request, "auctions/index.html", {"listings":listings.distinct(), 
    "category":category, "all_categories":all_categories})

@login_required
def add_comment(request):
    if request.method == "POST":
        listing_id= int(request.POST["listing_id"])
        this_listing = Listing.objects.get(id=listing_id)
        content = request.POST["content"]
        user = request.user
        time = datetime.datetime.now()
        new_comment=Comment(listing=this_listing, content=content, commenter=user, time=time)
        new_comment.save()
        return HttpResponseRedirect(reverse("product", args=(this_listing.id,)))

@login_required
def process_bid(request, listing_id):
    if request.method == "POST":
        this_listing = Listing.objects.get(id=listing_id)
        bids = this_listing.listingbid.all()
        new_bid_price = float(request.POST["NewBid"])
        bidder = request.user
        if not bids and new_bid_price>this_listing.start_price:
            n = Bid(bid_price=new_bid_price, bidder=bidder, 
            time=datetime.datetime.now(), listing=this_listing)
            n.save()
            messages.info(request, 'You Placed your Bid @ $')
            return HttpResponseRedirect(reverse("product", args=(this_listing.id,)))
        elif new_bid_price<=this_listing.start_price:
            return HttpResponseBadRequest("Bad Request: bidding price lower than start price")

        for bid in bids:
            bid_price=bid.bid_price
            if new_bid_price > bid_price:
                continue            
            elif new_bid_price <= bid_price:
                messages.info(request, 'You Bid is too low to be placed')
                return HttpResponseRedirect(reverse("product", args=(this_listing.id,)))
        n = Bid(bid_price=new_bid_price, bidder=bidder , 
        time=datetime.datetime.now(), listing=this_listing)
        n.save()
        messages.info(request, 'You Placed your Bid @ $%s' %new_bid_price)
        return HttpResponseRedirect(reverse("product", args=(this_listing.id,)))

