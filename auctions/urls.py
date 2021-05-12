from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("active_listings/<int:listing_id>", views.active_listings, name="active_listings"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("comment/<int:listingid>", views.comment, name="comment"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("remove_watchlist/<int:listingid>", views.remove_watchlist, name="remove_watchlist"),
    path("add_watchlist/<int:listingid>", views.add_watchlist, name="add_watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("deleted_listing/<int:listing_id>", views.deleted_listing, name="deleted_listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("fashion", views.fashion, name="fashion"),
    path("toy", views.toy, name="toy"),
    path("electronic", views.electronic, name="electronic"),
    path("home", views.home, name="home"),
    path("everything", views.everything, name="everything")
]

