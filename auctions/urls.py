from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("create_listing", views.create, name="create_listing"),
    path("login", views.login_view, name="login"),
	path("demo_login", views.demo, name="demo"),
    path("logout", views.logout_view, name="logout"),
    path("watch_list", views.watch_list, name="watch_list"),
    path("register", views.register, name="register"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("all_categories", views.categories, name="categories"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("won_listings", views.won_listings, name="won_listings"),
    path("category/<int:category_id>", views.show_category, name="category"),
    path("product/<int:product_id>", views.product, name="product"),
    path("<int:list_id>/remove_watch", views.stopwatch, name="stop_watch"),
    path("<str:list_title>/<str:listing_id>/close_listing", views.close_listing, name="close_listing"),
    path("<int:listing_id>/addtowatch", views.addwatch, name="add_watch"),
    path("<int:listing_id>/bids", views.process_bid, name="place_bid")
    

]
