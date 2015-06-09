from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.http import HttpResponseRedirect

admin.autodiscover()

import accounts.urls
import ajax.urls
import settings

def redirect_to(request):
	return HttpResponseRedirect('/index3/')

urlpatterns = patterns('',
    # Examples:
    url(r'^$',redirect_to),
    # url(r'^work/', include('work.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/',include(accounts.urls)),

	url(r'^ajax/',include(ajax.urls)),
	
	url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
#	(r'^test/$', personal_info)

)


urlpatterns += patterns('custom.views',
	(r'^index/$', 'index'),
	(r'^index2/$', 'index2'),
	(r'^index3/$', 'index'),

	(r'^editprofile/$', 'personal_info'),
	(r'^myorder/$', 'order_history'),
	(r'^myorder/(?P<page>\d+)/$', 'order_history'),
	(r'^recommands/$', 'recommands'),
	(r'^recommands/ajax/$','recommands',{'ajax':True}),
	(r'^current_order/$', 'current_order'),
	(r'^order/update/(?P<id>\d+)/$', 'order_update'),
	(r'^order/dup/(?P<id>\d+)/$', 'order_dup'),
	(r'^order/comfirm/$', 'order_comfirm'),
	(r'^order/committing/$', 'order_committing'), 
	(r'^errors_report/(?P<inval>\d+)/$', 'errors_report'),
	(r'^local_bank/$', 'local_bank'),
	(r'^food/spec/(?P<id>\d+)/(?P<page>\d+)/$', 'foodspec'),
	(r'^food/spec/(?P<id>\d+)/$', 'foodspec'),
)

urlpatterns+=patterns('custom.tv',
	url(r'^address/$','address'),
	url(r'^address/del/(?P<id>\d+)/$','address_del'),
	url(r'^address/(?P<id>\d+)/$','address'),

	url(r'^message/$','message'),
	url(r'^message/(?P<page>\d+)/$','message'),
	url(r'^message/outbox/$','message',{'type':1}),
	url(r'^message/outbox/(?P<page>\d+)/$','message',{'type':1}),
	url(r'^message/draft/$','message',{'type':2}),
	url(r'^message/draft/(?P<id>\d+)/$','message',{'type':2}),

	url(r'^message/edit/$','message_edit'),
	url(r'^message/edit/(?P<id>\d+)/$','message_edit'),

	url(r'^message/del/(?P<id>\d+)/$','message_del'),


	url(r'food/(?P<id>\d+)/$','food'),
)


