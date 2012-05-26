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
    url(r'^create_game/(?P<opponent_fb_id>\d+)$', 'app.views.create_game', name='create_game'),
    url(r'^games/$', 'app.views.list_games', name='list_games'),
    url(r'^games/(?P<game_id>\d+)$', 'app.views.game_details', name='game_details'),
    url(r'^$', 'app.views.index', name='index'),
    url(r'^users/$', 'app.views.show_users', name='show_users'),
    url(r'^users/(?P<user_id>\w+)/$', 'app.views.user_details', name='user_details'),
    url(r'^users/invite/(?P<user_id>\w+)/$', 'app.views.invite_user', name='invite_user'),
)

urlpatterns += patterns('',
    url(r'^login/', 'django_fukinbook.views.login', name='login'),
    url(r'^admin/', include(admin.site.urls)),
)
