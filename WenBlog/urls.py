# coding=utf8
"""WenBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from WenBlog import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', 'blog.views.index'),

    # name 是url的一个别称
    url(r'^page/(?P<page>\d+)/$', 'blog.views.index', name='view_blog_page'),

    url(r'^view/(?P<slug>.+)/$', 'blog.views.view_post', name='view_blog_post'),

    url(r'^category/(?P<slug>.+)/page/(?P<page>\d+)/$',
        'blog.views.view_category',
        name='view_blog_category_page'
        ),


    url(r'^category/(?P<slug>.+)/$',
        'blog.views.view_category',
        name='view_blog_category'
        ),

    url(r'^about_me/$', 'blog.views.about_me'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
]
