from django.conf.urls import patterns, include, url
from django.contrib import admin
from sakila_ok import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sakila.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sakila_ok.views.home', name='home'),
    url(r'^category/(?P<cat_id>\d+)$', 'sakila_ok.views.category', name='category'),
    url(r'^customer/$', 'sakila_ok.views.customer', name='customer'),
    url(r'^customer/(?P<cus_id>\d+)$', 'sakila_ok.views.customer', name='customer'),

    url(r'^film/$', 'sakila_ok.views.film', name='customer'),
    url(r'^film/(?P<film_id>\d+)$', 'sakila_ok.views.film', name='movie'),
    url(r'^film/search/$', 'sakila_ok.views.film_search', name='movie_search'),
)
