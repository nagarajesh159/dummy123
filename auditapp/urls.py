from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.IndexView.as_view()),
    path('countries/', views.CountryList.as_view()),
    path('countries/<int:country_id>/', views.CountryDetail.as_view()),
    path('countries/<int:country_id>/states/', views.StateList.as_view()),
    path('states/<int:state_id>/', views.StateDetail.as_view()),
    path('states/<int:state_id>/tags/', views.TagList.as_view()),
    path('tags/<int:tag_id>/', views.TagDetail.as_view()),
    path('tags/<int:tag_id>/urls/', views.URLList.as_view()),
    path('urls/<int:url_id>/', views.URLDetail.as_view()),
    path('states/', views.GetAllStates.as_view()),
    path('tags/', views.GetAllTags.as_view()),
    path('urls/', views.GetAllURLs.as_view()),


    path('save_datapoint/', views.GetAllURLs.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)