from django.db import models
from django.db.models import Q


class Swiped(models.Model):
    '''滑过的记录'''
    MARK = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )

    uid = models.IntegerField(db_index=True, verbose_name='用户自身 id')
    sid = models.IntegerField(db_index=True, verbose_name='被滑的陌生人 id')
    mark = models.CharField(max_length=16, db_index=True, choices=MARK, verbose_name='滑动类型')
    time = models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')

    class Meta:
        ordering = ['-time', 'uid', 'sid']

    @classmethod
    def is_liked(cls, uid, sid):
        condition = Q(mark='like') | Q(mark='superlike')
        if cls.objects.filter(condition, uid=uid, sid=sid).exists():
            return True
        return False

    @classmethod
    def swipe_right(cls, uid, sid):
        '''右滑'''
        defaults = {'mark': 'like'}
        cls.objects.update_or_create(uid=user.id, sid=stranger_id, defaults=defaults)

    @classmethod
    def swipe_up(cls, uid, sid):
        '''上滑'''
        defaults = {'mark': 'superlike'}
        cls.objects.update_or_create(uid=user.id, sid=stranger_id, defaults=defaults)

    @classmethod
    def swipe_left(cls, uid, sid):
        '''左滑'''
        defaults = {'mark': 'dislike'}
        cls.objects.update_or_create(uid=user.id, sid=stranger_id, defaults=defaults)

    @classmethod
    def liked(cls, uid):
        '''我喜欢过的'''
        condition = Q(mark='like') | Q(mark='superlike')
        return cls.objects.filter(condition, uid=uid)

    @classmethod
    def liked_me(cls, uid):
        '''喜欢我的'''
        condition = Q(mark='like') | Q(mark='superlike')
        return cls.objects.filter(condition, sid=uid)


class Friends(models.Model):
    '''
    好友关系表

    User 表自身的“多对多”关系, 有两个 uid 字段。
    为了数据量更精简，用户 A 与 用户 B 是好友关系只会产生一条记录，取其中较小的做 uid1, 较大的做 uid2
    '''
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def friend_id_list(cls, uid):
        condition = Q(uid1=uid) | Q(uid2=uid)
        relstions = cls.objects.filter(condition)
        fid_list = []
        for r in relstions:
            friend_id = r.uid2 if uid == r.uid1 else r.uid1
            fid_list.append(friend_id)
        return fid_list

    @classmethod
    def is_friends(cls, uid1, uid2):
        '''检查是否是朋友关系'''
        uid1, uid2 = sorted([uid1, uid2])
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def be_friends(cls, uid1, uid2):
        '''建立好友关系'''
        uid1, uid2 = sorted([uid1, uid2])
        cls.objects.get_or_create(uid1=uid1, uid2=uid2)

    @classmethod
    def break_off(cls, uid1, uid2):
        '''断绝好友关系'''
        uid1, uid2 = sorted([uid1, uid2])
        try:
            cls.objects.get(uid1=uid1, uid2=uid2).delete()
        except cls.DoesNotExists:
            pass

        condition = Q(uid=uid1, sid=uid2) | Q(uid=uid2, sid=uid1)
        Swiped.objects.filter(condition).update(mark='dislike')
