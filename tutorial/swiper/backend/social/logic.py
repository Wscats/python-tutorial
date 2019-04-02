from social.models import Swiped
from social.models import Friends

from user.models import User


def get_recommend_users(user):
    '''
    获取推荐列表

    TODO: 当前算法仅仅是随机筛选做的伪实现, 后期需要修改
    '''
    import random
    total = User.objects.count()
    start = random.randrange(total - 30)
    end = start + 30
    return User.objects.all()[start:end]


def like(user, stranger_id):
    '''喜欢'''
    Swiped.swipe_right(user.id, stranger_id)

    # 检查对方是否喜欢过自己
    if Swiped.is_liked(stranger_id, user.id):
        Friends.be_friends(user.id, stranger_id)
        # TODO: 向添加好友的双方实时推送消息
        return True
    else:
        return False


def superlike(user, stranger_id):
    '''超级喜欢'''
    Swiped.swipe_up(user.id, stranger_id)

    # 检查对方是否喜欢过自己
    if Swiped.is_liked(stranger_id, user.id):
        Friends.be_friends(user.id, stranger_id)
        # TODO: 向添加好友的双方实时推送消息
        return True
    else:
        return False


def dislike(user, stranger_id):
    '''不喜欢'''
    Swiped.swipe_left(user.id, stranger_id)


def rewind(user, stranger_id):
    '''反悔'''
    try:
        Swiped.objects.get(uid=user.id, sid=stranger_id).delete()
    except Swiped.DoesNotExist:
        pass


def get_users_liked_me(user):
    '''查看喜欢过过我的用户'''
    return Swiped.liked_me(user.id)
