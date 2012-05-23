from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'facecards.views.home', name='home'),
    # url(r'^facecards/', include('facecards.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^create_game/$', 'app.views.create_game', name='create_game'),
    url(r'^$', 'app.views.canvas', name='canvas'),
    url(r'^users/$', 'app.views.show_users', name='show_users'),
    url(r'^users/(?P<user_id>\d+)/$', 'app.views.user_details', name='user_details'),
)

urlpatterns += patterns('',
    url(r'^login/', 'django_fukinbook.views.login', name='login'),
    url(r'^canvas/', 'django_fukinbook.views.canvas', name='canvas'),
    url(r'^admin/', include(admin.site.urls)),
)
