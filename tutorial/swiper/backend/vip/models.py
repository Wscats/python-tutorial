from django.db import models


class Vip(models.Model):
    name = models.CharField(max_length=16, unique=True)
    level = models.IntegerField(unique=True, verbose_name='会员等级')
    price = models.FloatField(verbose_name='充值会员的价格, 单位：元')

    class Meta:
        ordering = ['level', 'name']

    def perms(self):
        relations = VipPermRelation.objects.filter(vip_id=self.id)
        perm_id = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id)

    def has_perm(self, perm_name):
        '''检查此 VIP 是否具有某种权限'''
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False


class Permission(models.Model):
    '''
    用户特权
        superlike 超级喜欢的权限
        rewind    反悔的权限
        likeme    查看谁喜欢我的权限
    '''
    name = models.CharField(max_length=32)
    description = models.TextField(verbose_name='权限详情介绍')


class VipPermRelation(models.Model):
    '''
    VIP-Permission 关系表

    每级 VIP 对应的权限
        VIP1: 超级喜欢权限
        VIP2: 全部 VIP1 的权限 + 反悔权限
        VIP3: 全部 VIP2 的权限 + 查看被喜欢权限

    NOTE:
        如果需要可以将权限做的更细，每种权限限制每天的使用次数。
        比如 VIP1 每日反悔 3 次，VIP2 每日反悔 10 次
    '''
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_relation(cls, vip_name, perm_name):
        vip = Vip.get(name=vip_name)
        perm = Permission.get(name=perm_name)
        cls.get_or_create(vip_id=vip_id, perm_id=perm_id)

    @classmethod
    def del_relation(cls, vip_name, perm_name):
        vip = Vip.get(name=vip_name)
        perm = Permission.get(name=perm_name)
        try:
            cls.get(vip_id=vip_id, perm_id=perm_id).delete()
        except cls.DoesNotExist:
            pass
