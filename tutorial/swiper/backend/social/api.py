from lib.http import require_post
from lib.http import render_json
from vip.logic import need_perm
from social import logic
from social.models import Friends


def recommend(request):
    '''获取推荐列表'''
    users = logic.get_recommend_users(request.user)
    return render_json({'users': [u.to_dict() for u in users]})


@require_post
def like(request):
    '''喜欢'''
    stranger_id = int(request.POST.get('stranger_id'))
    return render_json({'matched': logic.like(stranger_id)})


@require_post
@need_perm('superlike')
def superlike(request):
    '''超级喜欢'''
    stranger_id = int(request.POST.get('stranger_id'))
    return render_json({'matched': logic.superlike(stranger_id)})


@require_post
def dislike(request):
    '''不喜欢'''
    stranger_id = int(request.POST.get('stranger_id'))
    logic.dislike(stranger_id)
    return render_json()


@require_post
@need_perm('rewind')
def rewind(request):
    '''反悔'''
    stranger_id = int(request.POST.get('stranger_id'))
    return render_json(logic.rewind(stranger_id))


@need_perm('liked_me')
def who_liked_me(request):
    '''查看谁喜欢过我'''
    users = logic.get_users_liked_me(request.user)
    return render_json({'users': users})


def friend_list(request):
    '''好友列表'''
    user = request.user
    friends = [f.to_dict() for f in user.friends()]
    return render_json({'friends': friends})


@require_post
def break_off(request):
    '''与对方绝交'''
    stranger_id = int(request.POST.get('stranger_id'))
    Friends.break_off(request.session.uid, stranger_id)
    return render_json()
