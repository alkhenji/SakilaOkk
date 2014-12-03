from django.conf.urls import patterns, include, url
from django.contrib import admin
from sakila_ok import views

handler404 = 'sakila_ok.views.error404'
handler500 = 'sakila_ok.views.error500'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sakila.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sakila_ok.views.home', name='home'),
    url(r'^category/(?P<cat_id>\d+)$', 'sakila_ok.views.category', name='category'),
    url(r'^customer/$', 'sakila_ok.views.customer', name='customer'),
    url(r'^customer/(?P<cus_id>\d+)$', 'sakila_ok.views.customer', name='customer'),

    url(r'^customer/(?P<cus_id>\d+)/pay/$', 'sakila_ok.views.pay', name='pay'),

    # url(r'^customer/(?P<cus_id>\d+)/(?<film_id>)/(?<_id>)/$', 'sakila_ok.views.cap', name='cap'),

    # url(r'^customer/(?P<cus_id>\d+)/cnp/$', 'sakila_ok.views.cap', name='cnp'),
    # url(r'^customer/(?P<cus_id>\d+)/cnp/(?<film_id>)$', 'sakila_ok.views.cap2', name='cnp2'),

    # url(r'^customer/(?P<cus_id>\d+)/pay/$', 'sakila_ok.views.cap', name='cnp'),

    # url(r'^customer/(?P<cus_id>\d+)/return/$', 'sakila_ok.views.cap', name='cnp'),

    url(r'^film/$', 'sakila_ok.views.film', name='customer'),
    url(r'^film/(?P<film_id>\d+)$', 'sakila_ok.views.film', name='movie'),
    url(r'^film/search/$', 'sakila_ok.views.film_search', name='movie_search'),
)