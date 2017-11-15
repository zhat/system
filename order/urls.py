from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^search_by_name/$',views.search_by_name,name='search_by_name'),
    url(r'^search_by_profile/$',views.search_by_profile,name='search_by_profile'),
    url(r'^search_by_name_and_profile/$',views.search_by_name_and_profile,name='search_by_name_and_profile'),
    url(r'^advise/$',views.add_advise,name='advise'),
    url(r'^$',views.search_by_profile,name='index'),
]