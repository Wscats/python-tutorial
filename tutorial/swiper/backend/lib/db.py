from django.db import models

from lib.cache import rds
from common.keys import MODEL_KEY


def get(cls, *args, **kwargs):
    '''数据优先从缓存获取, 缓存取不到再从数据库获取'''
    # 创建 key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 从缓存获取
    if pk is not None:
        key = MODEL_KEY % (cls.__name__, pk)
        model_obj = rds.get(key)
        if isinstance(model_obj, cls):
            return model_obj

    # 缓存里没有，直接从数据库获取，同时写入缓存
    model_obj = cls.objects.get(*args, **kwargs)
    key = MODEL_KEY % (cls.__name__, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj


def get_or_create(cls, *args, **kwargs):
    # 创建 key
    pk = kwargs.get('pk') or kwargs.get('id')

    # 从缓存获取
    if pk is not None:
        key = MODEL_KEY % (cls.__name__, pk)
        model_obj = rds.get(key)
        if isinstance(model_obj, cls):
            return model_obj, False

    # 执行原生方法，并添加缓存
    model_obj, created = cls.objects.get_or_create(*args, **kwargs)
    key = MODEL_KEY % (cls.__name__, model_obj.pk)
    rds.set(key, model_obj)
    return model_obj, created


def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    '''存入数据库后，同时写入缓存'''
    self._ori_save(force_insert, force_update, using, update_fields)

    # 添加缓存
    key = MODEL_KEY % (self.__class__.__name__, self.pk)
    rds.set(key, self)


def to_dict(self, *ignore):
    '''获取对象的属性字典'''
    attr_dict = {}
    for field in self._meta.fields:
        if field.name in ignore:
            continue
        attr_dict[field.name] = getattr(self, field.name)
    return attr_dict


def patch_model():
    '''
    动态更新 Model 方法

    Model 在 Django 中是一个特殊的类, 如果通过继承的方式来增加或修改原有方法, Django 会将
    继承的类识别为一个普通的 app.model, 所以只能通过 monkey patch 的方式动态修改
    '''
    # 动态添加一个类方法 get
    models.Model.get = classmethod(get)
    models.Model.get_or_create = classmethod(get_or_create)

    # 修改 save
    models.Model._ori_save = models.Model.save
    models.Model.save = save

    # 添加 to_dict
    models.Model.to_dict = to_dict
