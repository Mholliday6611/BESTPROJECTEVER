from django.conf.urls import patterns, url
from appone import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'soloproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
 #    url(r'^post/', views.post, name='post')
 #    url(r'^add-post/',views.AddPost name='addpost')
 #    url(r'^about/', views.about, name='about'),
 #    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
 #    url(r'^category/(?P<category_name_slug>[\w\-]+)/add-page/$', views.add_page, name='add-page'),
 #    url(r'^register/', views.register, name='register'),
 #    url(r'^login/', views.user_login, name='login'),
 #    url(r'^logout/', views.user_logout, name='logout'),
 #    url(r'^goto/$', views.track_url, name='goto'),
 #    url(r'^user/(?P<user_username>[\w\-]+)/$',views.user_profile, name='profile'),
 #    url(r'^user/(?P<user_username>[\w\-]+)/edit/$',views.edit_profile, name='edit_profile'),
 #    url(r'^contact/$', views.contact, name='contact'),
 #    url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
 #    url(r'^recover-password/$', views.PasswordRecoveryView.as_view(), name='recover-password'),
     )
