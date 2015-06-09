from django.conf.urls.defaults import patterns, include, url
from views import *
from django.contrib.auth.views import login,logout,password_change,password_change_done,password_reset,password_reset_done

urlpatterns = patterns('',
    url(r'^register/$', register),

	#url(r'^$',login,{'template_name':'login.html'}),
	url(r'^$',sitemap),
	url(r'^profile/$',sitemap),
	url(r'^login/$',login,{'template_name':'login.html'}),

	url(r'^logout/$',logout,{'template_name':'logout.html'}),

	url(r'^password_change/$',password_change,
		{
			'post_change_redirect':'/accounts/password_change_done/',
			'template_name':'password_change.html'
		}),

	url(r'^password_change_done/$',password_change_done,
		{'template_name':'password_change_done.html'}),
	url(r'^password_reset/$',password_reset,
		{
			'post_reset_redirect':'/accounts/password_reset_done/',
			'template_name':'password_reset.html',
			'email_template_name':'password_reset.html',
			'from_email':'zwzmzd@mail.enjoy-what.com',
		}),
	url(r'^password_reset_done/$',password_reset_done,
		{'template_name':'password_reset_done.html'}),

	url(r'^set_email/$',set_email),
)
