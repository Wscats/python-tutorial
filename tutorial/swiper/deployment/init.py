#!/usr/bin/env python

import os
import sys
import random

import django

# 设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')

sys.path.insert(0, BACKEND_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
django.setup()


from user.models import User

last_names = (
    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨'
    '朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎'
    '鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常'
    '乐于时傅皮卞齐康伍余元卜顾孟平黄'
)

first_names = {
    'Male': [
        '致远', '俊驰', '雨泽', '烨磊', '晟睿',
        '天佑', '文昊', '修洁', '黎昕', '远航',
        '旭尧', '鸿涛', '伟祺', '荣轩', '越泽',
        '浩宇', '瑾瑜', '皓轩', '浦泽', '绍辉',
        '绍祺', '升荣', '圣杰', '晟睿', '思聪'
    ],
    'Female': [
        '沛玲', '欣妍', '佳琦', '雅芙', '雨婷',
        '韵寒', '莉姿', '雨婷', '宁馨', '妙菱',
        '心琪', '雯媛', '诗婧', '露洁', '静琪',
        '雅琳', '灵韵', '清菡', '溶月', '素菲',
        '雨嘉', '雅静', '梦洁', '梦璐', '惠茜'
    ]
}


def rand_name():
    last_name = random.choice(last_names)
    sex = random.choice(['Male', 'Female'])
    first_name = random.choice(first_names[sex])
    return ''.join([last_name, first_name]), sex


# 创建初始用户
for i in range(1000):
    name, sex = rand_name()
    User.objects.create(
        phonenum='%s' % random.randrange(21000000000, 21900000000),
        nickname=name,
        sex=sex,
        birth_year=random.randint(1980, 2000),
        birth_month=random.randint(1, 12),
        birth_day=random.randint(1, 28),
        location=random.choice(['北京', '上海', '深圳', '成都', '西安', '沈阳', '武汉']),
    )
    print('created: %s %s' % (name, sex))
