from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.blog,name= "index"),
    path('<int:pid>',views.blog_single,name= "single"),
    path('category/<str:cat_name>',views.blog,name= "category"),
    path('author/<str:author_username>',views.blog,name= "author"),
    path('search/',views.search,name= "search"),

]
