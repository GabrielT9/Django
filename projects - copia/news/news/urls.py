from django.conf.urls import patterns, include, url
#from django.views.generic.simple import direct_to_template
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'news.views.home', name='home'),
    # url(r'^news/', include('news.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', 'polls.views.show_home', name='home'),
    url(r'^$', 'polls.views.show_foda', name='home'),
    (r'^register/$', 'polls.views.PersonRegistration'),
    (r'^login/$', 'polls.views.LoginRequest'),
    (r'^logout/$', 'polls.views.LogoutRequest'),
    (r'^resetpassword/passwordsent/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^news/$', 'polls.views.NewsCreate'),
    (r'^profile/$', 'polls.views.Profile'),
    (r'^comment/(?P<id>\d+)/$$', 'polls.views.CommentCreate'),
    (r'^listnews/$', 'polls.views.show_news'),
    (r'^detailnews/(?P<id>\d+)/$', 'polls.views.detail_news'),
    (r'^deletenews/(?P<id>\d+)/$', 'polls.views.NewsDelete'),
    (r'^listcomments/(?P<id>\d+)/$', 'polls.views.show_comments'),
    (r'^mycomments/(?P<id>\d+)/$', 'polls.views.show_my_comments'),
    (r'^deletecomms/(?P<id>\d+)/$', 'polls.views.CommentsDelete'),
    (r'^detailmycomms/(?P<id>\d+)/$', 'polls.views.detail_my_comms'),
    (r'^mynews/$', 'polls.views.show_my_news'),
    (r'^detailmynews/(?P<id>\d+)/$', 'polls.views.detail_my_news'),
    (r'^updatenews/(?P<id>\d+)/$', 'polls.views.edit_news'),
)