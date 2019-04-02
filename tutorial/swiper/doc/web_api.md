前后端接口
==========

## 接口格式

1. 所有获取数据的 HTTP 接口, 参数均由 GET 方法传递
2. 所有修改数据的 HTTP 接口, 参数均由 POST 方法传递
3. 返回值均为 JSON 格式, 必须包含两个字段: "code", "data"
    1. code 字段为状态码(status code), int 类型, 为 0 时表示返回值正常, 其他任何值时均表示异常, 需客户端根据状态码为用户提供不同的错误提示
    2. data 字段为返回的数据, 字典类型. 详情见下面具体接口. 当一个接口仅需状态码确认时, data 可以为空
    3. 示例
       ```json
       {
           "code": 0,
           "data": {
               "user": {
                   "uid": 123321,
                   "username": "Lion",
                   "age": 21,
                   "sex": "Male"
                },
               "date": "2018-09-12",
           }
       }
       ```

## status 状态码

code | description
-----|-------------
   0 | 正常
1000 | 服务器内部错误
1001 | 参数错误
1002 | 数据错误
1003 | 不存在
1004 | 达到上限
1005 | 没有权限
1006 | 超时
1007 | 已过期
1008 | 时间未到
1009 | 无效验证码
2000 | 用户未登录
2001 | 名字冲突
2002 | 金钱不足
2003 | 用户不存在
2004 | 不是好友关系


## 基础数据格式

1. User
    ```json
    {
        "uid": 123,                   // 用户 id
        "nickname": "Miao",           // 用户名
        "age": 21,                    // 年龄
        "sex": "M",                   // 性别
        "location": "China/Beijing",  // 常居地
        "avatars": [                  // 头像 URL 列表, 最多为 6 张
            "http://xxx.com/user/avatar/123/1.jpg",
            "http://xxx.com/user/avatar/123/2.jpg",
            "http://xxx.com/user/avatar/123/3.jpg",
            ...
        ]
    }
    ```

## User 接口

1. 提交手机号
    * **Description**: 提交手机号，根据结果判断下一步需要提交的数据
    * **Method**: POST
    * **Path**: /user/verify
    * **Params**:

        field | required | type | description
        ------|----------|------|-----------------------
        phone | Yes      |  str | 手机号, "18888888888"

    * **Return**:

        data 为 null

        ```json
        {
            "code": 0,
            "data": null
        }
        ```

2. 提交验证码登录
    * **Description**: 根据上一步的结果提交需要的数据
    * **Method**: POST
    * **Path**: /user/login
    * **Params**:

        field | required | type | description
        ------|----------|------|-----------------------
        phone | Yes      |  int | 手机号
         code | Yes      |  int | 验证码

    * **Return**:

        field | required | type | description
        ------|----------|------|-----------------------
         user | Yes      | User | 用户数据

        示例:
        ```json
        {
            "code": 0,
            "data": {
                "user": {
                    "uid": 123,                   // 用户 id
                    "nickname": "Miao",           // 用户名
                    "age": 21,                    // 年龄
                    "sex": "M",                   // 性别
                    "location": "China/Beijing",  // 常居地
                    "avatars": [                  // 头像 URL 列表, 最多为 6 张
                        "http://xxx.com/user/avatar/123/1.jpg",
                        "http://xxx.com/user/avatar/123/2.jpg",
                        "http://xxx.com/user/avatar/123/3.jpg",
                        ...
                    ]
                },
            },
        }
        ```

3. 获取配置信息
    * **Description**: -
    * **Method**: GET
    * **Path**: /user/profile/show
    * **Params**: 无需参数

    * **Return**:

        field          | required | type  | description
        ---------------|----------|-------|-----------------------
        location       | Yes      | str   |  目标城市
        min_distance   | Yes      | float |  最小查找范围
        max_distance   | Yes      | float |  最大查找范围
        min_dating_age | Yes      | int   |  最小交友年龄
        max_dating_age | Yes      | int   |  最大交友年龄
        dating_sex     | Yes      | str   |  匹配的性别
        vibration      | Yes      | bool  |  开启震动
        only_matche    | Yes      | bool  |  不让为匹配的人看我的相册
        auto_play      | Yes      | bool  |  自动播放视频

4. 修改配置
    * **Description**: 需要修改哪个就传哪个, 虽然参数均为非必选参数, 但至少传一个
    * **Method**: POST
    * **Path**: /user/profile/update
    * **Params**:

        field          | required | type  | description
        ---------------|----------|-------|-----------------------
        location       |    No    | str   |  目标城市
        min_distance   |    No    | float |  最小查找范围
        max_distance   |    No    | float |  最大查找范围
        min_dating_age |    No    | int   |  最小交友年龄
        max_dating_age |    No    | int   |  最大交友年龄
        dating_sex     |    No    | str   |  匹配的性别
        vibration      |    No    | bool  |  开启震动
        only_matche    |    No    | bool  |  不让为匹配的人看我的相册
        auto_play      |    No    | bool  |  自动播放视频

    * **Return**:

        data 为 null

5. 上传头像
    * **Description**: 至少上传一张
    * **Method**: POST
    * **Path**: /user/avatar/upload
    * **Params**:

        field  | required | type | description
        -------|----------|------|-----------------------
        first  |  No      |  str | 第一张
        second |  No      |  str | 第二张
        third  |  No      |  str | 第三张
        fourth |  No      |  str | 第四张
        fifth  |  No      |  str | 第五张
        sixth  |  No      |  str | 第六张

    * **Return**:

        data 为 null


## Social 接口

1. 获取推荐用户
    * **Description**:
    * **Method**: GET
    * **Path**: /social/recommend
    * **Params**: 无需参数

    * **Return**:

        field | required | type      | description
        ------|----------|-----------|-----------------------
        users | Yes      | User List | 用户数据列表

        示例:

        ```json
        {
            "code": 0,
            "data": {
                "users": [
                    {"uid": 123, "nickname": "Da", "age": 21, ...},
                    {"uid": 456, "nickname": "Miao", "age": 21, ...},
                    ...
                ],
            }
        }
        ```


2. 喜欢
    * **Description**:
    * **Method**: POST
    * **Path**: /social/like
    * **Params**:

        field       | required | type | description
        ------------|----------|------|-----------------------
        stranger_id | Yes      |  int | 被滑用户的 uid

    * **Return**:

        field   | required | type | description
        --------|----------|------|-----------------------
        matched | Yes      | bool | 是否与此用户匹配

3. 超级喜欢
    * **Description**:
    * **Method**: POST
    * **Path**: /social/superlike
    * **Params**:

        field       | required | type | description
        ------------|----------|------|-----------------------
        stranger_id | Yes      |  int | 被滑用户的 uid

    * **Return**:

        field   | required | type | description
        --------|----------|------|-----------------------
        matched | Yes      | bool | 是否与此用户匹配

4. 不喜欢
    * **Description**:
    * **Method**: POST
    * **Path**: /social/dislike
    * **Params**:

        field       | required | type | description
        ------------|----------|------|-----------------------
        stranger_id | Yes      |  int | 被滑用户的 uid

    * **Return**:

        data 为 null

5. 反悔
    * **Description**:
    * **Method**: POST
    * **Path**: /social/rewind
    * **Params**:

        field       | required | type | description
        ------------|----------|------|-----------------------
        stranger_id | Yes      |  int | 被滑用户的 uid

    * **Return**:

        data 为 null

6. 查看谁喜欢过我
    * **Description**:
    * **Method**: GET
    * **Path**: social/likedme
    * **Params**: 无需参数

    * **Return**:

        field | required | type      | description
        ------|----------|-----------|-----------------------
        users | Yes      | User List | 喜欢过我的用户数据列表

        示例:
        ```json
        {
            "code": 0,
            "data": {
                "users": [
                    {"uid": 123, "nickname": "Da", "age": 21, ...},
                    {"uid": 456, "nickname": "Miao", "age": 21, ...},
                    ...
                ]
            }
        }
        ```

7. 查看好友列表
    * **Description**:
    * **Method**: GET
    * **Path**: social/friends
    * **Params**: 无需参数

    * **Return**:

        field   | required | type      | description
        --------|----------|-----------|-----------------------
        friends | Yes      | User List | 我的好友数据列表

        示例:
        ```json
        {
            "code": 0,
            "data": {
                "friends": [
                    {"uid": 123, "nickname": "Da", "age": 21, ...},
                    {"uid": 456, "nickname": "Miao", "age": 21, ...},
                    ...
                ]
            }
        }
        ```

8. 断绝好友关系
    * **Description**:
    * **Method**: POST
    * **Path**: social/break_off
    * **Params**:

        field       | required | type | description
        ------------|----------|------|-----------------------
        stranger_id | Yes      |  int | 要绝交的用户 uid

    * **Return**:

        data 为 null
