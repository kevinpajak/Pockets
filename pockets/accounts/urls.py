
from django.conf.urls import patterns, url
from accounts import views


activation = "(?P<uidb36>[-\w]+)/(?P<token>[-\w]+)"
urlpatterns = patterns('',
                       #url(r'^$', views.index, name='index'),
                       url(r'^signup/$', views.signup, name='signup'),
                       url(r'^login/$', views.login, name='login'),
                       url(r'^profile/$', views.profile, name='profile'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^activate/%s/$' % (activation,), views.activate_account, name="activate"),
                       )