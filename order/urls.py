from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'advise/$',views.add_advise,name='advise'),
    url(r'',views.search,name='search'),
]