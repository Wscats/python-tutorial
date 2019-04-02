import datetime

from django.db import models
from django.utils.functional import cached_property

from vip.models import Vip
from social.models import Friends


class User(models.Model):
    SEX = (
        ('Male', '男'),
        ('Female', '女'),
    )

    phonenum = models.CharField(max_length=16, unique=True)
    nickname = models.CharField(max_length=16)

    # user info
    sex = models.CharField(max_length=16, choices=SEX, blank=False, null=False)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    location = models.CharField(max_length=32, verbose_name='常居地')

    vip_id = models.IntegerField(default=1)  # 关联的 vip id
    vip_expiration = models.DateTimeField(auto_now_add=True, verbose_name="会员过期时间")

    def init(self):
        '''TODO: 创建新用户的初始化操作'''
        pass

    @cached_property
    def age(self):
        '''年龄'''
        birthday = datetime.date(self.birth_year, self.birth_month, self.birth_day)
        return (datetime.date.today() - birthday).days // 365

    @cached_property
    def avatar(self):
        '''头像'''
        return Avatar.get_or_create(id=self.id)[0]

    @cached_property
    def profile(self):
        '''资料'''
        return Profile.get_or_create(id=self.id)[0]

    @cached_property
    def vip(self):
        '''用户会员'''
        return Vip.get(id=self.vip_id)

    @cached_property
    def friends(self):
        '''用户的好友列表'''
        fid_list = Friends.friend_id_list(self.id)
        return User.objects.filter(id__in=fid_list)  # objects 是特殊的类属性, 只能通过类调用

    @cached_property
    def is_dating_ready(self):
        '''检查资料是否完整'''
        pass

    def to_dict(self):
        return {
            'uid': self.id,
            'nickname': self.nickname,
            'age': self.age,
            'sex': self.sex,
            'location': self.location,
            'avatars': list(self.avatar),
        }


class Avatar(models.Model):
    '''
    用户形象

    与 User 是“一对一”关系，直接与 User 表 id 保持一致
    '''
    first = models.URLField(null=True, blank=True)
    second = models.URLField(null=True, blank=True)
    third = models.URLField(null=True, blank=True)
    fourth = models.URLField(null=True, blank=True)
    fifth = models.URLField(null=True, blank=True)
    sixth = models.URLField(null=True, blank=True)

    def __iter__(self):
        urls = [self.first, self.second, self.third,
                self.fourth, self.fifth, self.sixth]
        return filter(None, urls)  # 取出非空头像

    @cached_property
    def head(self):
        '''选择第一张图片作为头像'''
        return self.first


class Profile(models.Model):
    '''
    用户个人配置

    与 User 是“一对一”关系，直接与 User 表 id 保持一致
    '''
    SEX = (
        ('Male', '男性'),
        ('Female', '女性'),
        ('All', '不限'),
    )

    # 交友设置
    location = models.CharField(max_length=32, verbose_name='目标城市')
    min_distance = models.FloatField(default=1.0, verbose_name='最小查找范围')
    max_distance = models.FloatField(default=50.0, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    dating_sex = models.CharField(max_length=16, choices=SEX, verbose_name='匹配的性别')

    # 其他设置
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=False, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=False, verbose_name='自动播放视频')
