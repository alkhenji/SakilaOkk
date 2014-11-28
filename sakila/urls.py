from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sakila.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sakila.views.home', name='home'),
    url(r'^category/(?P<cat_id>\d+)$', 'sakila_ok.views.category', name='category'),
    url(r'^customer/$', 'sakila_ok.views.customer', name='customer'),
    url(r'^customer/(?P<cus_id>\d+)$', 'sakila_ok.views.customer', name='customer'),
)
