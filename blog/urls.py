from django.conf.urls import url, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^$', views.post_list, name='post_list'),
    url(r'^$', views.home, name='home'),
    url(r'^categories/$', views.post_categories, name='post_categories'),
    url(r'^about/$', views.about, name='about'),
    url(r'^gallery/$', views.gallery, name='gallery'),
    url(r'^home/$', views.post_list, name='post_list'),
    url(r'^categories/vegan/$', views.vegan, name='vegan'),
    url(r'^categories/dessert/$', views.dessert, name='dessert'),
    url(r'^categories/quick/$', views.quick, name='quick'),
    url(r'^categories/dinner/$', views.dinner, name='dinner'),
    url(r'^categories/soup/$', views.soup, name='soup'),
    url(r'^categories/salad/$', views.salad, name='salad'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^profile/(?P<pk>\d+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<pk>\d+)/settings/$', views.profile_settings, name='profile_settings'),
    url(r'^profile/(?P<pk>\d+)/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^profile/(?P<pk>\d+)/password/$', views.password, name='password'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friend, name='change_friend'),
    url(r'^friends/(?P<pk>\d+)/$', views.friends_list, name='friends_list'),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

