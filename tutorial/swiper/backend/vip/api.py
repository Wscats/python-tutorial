from vip.models import Vip


def vip_info(request):
    '''枚举所有 VIP 的权限'''
    vips = {}
    for vip in Vip.objects.all():
        perms = ((perm.name, perm.description) for perm in vip.perms())
        vips[vip.level] = {'price': vip.price, 'perms': sorted(perms)}
    return vips
