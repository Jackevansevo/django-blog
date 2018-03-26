from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    # Search view
    path('search/', views.post_search, name='post_search'),
    # Publish end point
    path('publish/<int:pk>/', views.post_publish, name='post_publish'),
    # Post detail
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    # RSS/Atom feed
    path('latest/feed/', views.LatestPostsFeed(), name='rss_feed'),
    # Tag detail
    path('tagged/<slug:slug>/', views.tag_detail, name='tag_detail'),
    # Archive views
    path('<int:year>/<int:month>/', views.PostMonthArchiveView.as_view(month_format='%m'), name="archive_month_numeric"),
    # Example: /2012/aug/
    path(
        '<int:year>/<str:month>/',
        views.PostMonthArchiveView.as_view(),
        name="archive_month",
    ),
]
