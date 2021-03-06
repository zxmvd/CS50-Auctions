This Django project is an <strong>eBay-like e-commerce auction site</strong> that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”<br>

<a href="https://mini-auctions.herokuapp.com" target="_blank"><strong>Live Demo</strong></a><br>
- In <a href="auctions/models.py">auctions/models.py</a> are Django Modeles and its fields.
- In <a href="auctions/urls.py">auctions/urls.py</a>, the URL configuration for this app is defined.
- In <a href="auctions/views.py">auctions/views.py</a> functions will return results to the web browser.
- In <a href="auctions/templates/auctions">auctions/templates/auctions/</a> are templates inheriting from a base layout.html file.
- CSS is in <a href="auctions/static/auctions/style.scss">auctions/static/auctions/</a>.
<hr>
<a href="https://mini-auctions.herokuapp.com/product/2"><img src="staticfiles/screenshot.png" width="900"></a>
<hr>

* Create Listing: Users will be able to visit a page to create a new listing. 
* Active Listings Page: The default route of the web application, will let users view all of the currently active auction listings.
* Listing Page: 
  - Shows all details about the listing, including the current price for the listing. 
  - User can add/remove the item to/from their “Watchlist.” 
  - User can bid on the item.
  - Listing owner can “close” the auction from this page, which makes the highest bidder the winner of the auction.
  - Signed in users can add comments to the listing page. 
* Watchlist: Users who are signed in can visit a Watchlist page.
* Categories: Users can visit a page showing all listings of a selected category. 


