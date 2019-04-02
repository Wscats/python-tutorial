"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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

from user import api as user_api
from social import api as social_api
from vip import api as vip_api


urlpatterns = [
    # User API
    url(r'^api/user/verify$', user_api.verify_phone),
    url(r'^api/user/login$', user_api.login),
    url(r'^api/user/profile/show$', user_api.show_profile),
    url(r'^api/user/profile/update$', user_api.update_profile),
    url(r'^api/user/avatar/upload$', user_api.upload_avatar),
    # WeiBo
    url(r'weibo/authurl$', user_api.weibo_authurl),
    url(r'weibo/callback$', user_api.weibo_callback),

    # Social API
    url(r'api/social/recommend$', social_api.recommend),
    url(r'api/social/like$', social_api.like),
    url(r'api/social/superlike$', social_api.superlike),
    url(r'api/social/dislike$', social_api.dislike),
    url(r'api/social/rewind$', social_api.rewind),
    url(r'api/social/likedme$', social_api.who_liked_me),
    url(r'api/social/friends$', social_api.friend_list),
    url(r'api/social/break_off$', social_api.break_off),

    # VIP API
    url(r'api/vip/info$', vip_api.vip_info),
]
