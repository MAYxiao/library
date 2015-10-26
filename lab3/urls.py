from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lab3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'lab3.library.views.index'),
    url(r'^ClassRoom/add/$', 'lab3.library.views.ClassroonAdd'),  
    url(r'^admin/', include(admin.site.urls)),
)
