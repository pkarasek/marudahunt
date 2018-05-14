from django.urls import path, include
from . import views

urlpatterns = [

    path('create', views.create, name = "create"),
    path('<int:maruda_id>', views.detail, name = "detail"),
    path('<int:maruda_id>/upvote', views.upvote, name = "upvote"),
    path('topfive', views.topfive, name = "topfive"),

]
