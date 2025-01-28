from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.index, name="index"),
    path("listing/create", views.create_listing, name="create_listing"),
    path("listing/<str:listing_id>", views.show_listing, name="show_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
