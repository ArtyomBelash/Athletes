from django.urls import path
from .views import *

urlpatterns = [
    path('', AthletesListView.as_view(), name='index'),
    path('athlete/<slug:athlete_slug>/', AthleteDetailView.as_view(), name='detail'),
    path('category/<slug:cat_slug>/', CategoryAthletesListView.as_view(), name='category'),
    path('add_athlete/', NewAthlete.as_view(), name='add_athlete'),
    path('search/', SearchAthlete.as_view(), name='search_athlete'),
    path('share/<slug:athlete_slug>/', post_share, name='post_share'),
    path('like/', athlete_like, name='like'),
    path('likes/', AthletesLikes.as_view(), name='likes'),
]
