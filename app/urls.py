from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^ajax/post-message/$', views.post_message, name='ajax_post_message'),
    url(r'^ajax/get-activity/$', views.get_activity, name='ajax_get_activity'),
]
