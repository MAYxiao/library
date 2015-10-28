from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lab3.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'lab3.library.views.index'),
    url(r'^delete.html/$', 'lab3.library.views.delete'),
    url(r'^update.html/$', 'lab3.library.views.update'),
    url(r'^abinfo.html/$', 'lab3.library.views.bookinfo'),
    url(r'^ClassRoom/add/$', 'lab3.library.views.ClassroonAdd'),
    url(r'^admin/', include(admin.site.urls)),
)
