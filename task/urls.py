from django.conf.urls import patterns, url
from task import views

urlpatterns = patterns('',
        url(r'^$', views.list_of_tasks, name='list_of_tasks'),
        url(r'^create_task/', views.create_task, name='create_task'),
        url(r'^list_of_tasks/', views.list_of_tasks, name='list_of_tasks'),
        url(r'^create_report/', views.create_report, name='create_report'),
        url(r'^send_message/', views.send_message, name='send_message'),
        url(r'^show_detail/', views.show_detail, name='show_detail'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^admin/', views.admin, name='admin'),
        url(r'^admin_detail/(?P<emp_id>[0-9]+)/',views.admin_detail, name='admin_detail'),
        url(r'^admin_show_detail/(?P<emp_id>[0-9]+)/', views.admin_show_detail, name='admin_show_detail'),
        url(r'^admin_create_task/(?P<emp_id>[0-9]+)/', views.admin_create_task, name='admin_create_task'),
        url(r'^admin_create_report/(?P<emp_id>[0-9]+)/', views.admin_create_report, name='admin_create_report'),
)