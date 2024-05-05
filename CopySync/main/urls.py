from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("view/<str:url>", views.paste, name="paste"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("view/", views.view_paste, name="view_paste"),
    path("delete/<str:url>", views.delete_paste, name="delete_paste"),
]
