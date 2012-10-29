from django.conf.urls import patterns, include, url
from filebrowser.sites import site
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth.views import logout
#from django.views.generic.simple import direct_to_template
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), 
    url(r'^admin/', include(admin.site.urls)),

    url(r'^upload/$','upload.views.uploadfile',name="index"),
    url(r'^upload/delete/(?P<id>\w+)$','upload.views.deleteDoc',name="idel"),
    url(r'^upload/doc/(?P<id>\w+)/$','upload.views.detail',name="doc"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    url(r'^login/$','django.contrib.auth.views.login', {'template_name': 'login.html'},name='login'), 
    url(r'^register/$',  'upload.views.register',  name="register"), 
    url(r'^activate/$',  'upload.views.activate',  name="activate"), 
    url(r'^logout/$',  logout,{'next_page': '/upload/'}, name="logout"), 
    url(r'^goto/(?P<id>\w+)/(?P<filename>.+)/$', 'upload.views.goto' ),
    url(r'^user/(?P<username>\w+)/$', 'upload.views.ShowProfile' ),
    

)
