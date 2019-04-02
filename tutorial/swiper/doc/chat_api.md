WebSocket 通信协议
==================

## 统一数据包格式

数据包整体为一个二元 json 列表, 第一位为包的标识, 字符串类型, 第二位是具体数据
如 '发送私聊消息':
```python
[
    'PRIVATE',                          # tag
    {'to': '112233', 'msg': 'abcdefg'}  # data
]
```

## 协议详情

### 1. 私人聊天

* **tag**: PRIVATE
* **data**: 消息体，分为发送包和接收包两种状况
* **示例**:
    - 消息发送方:
        ```python
        [
            'PRIVATE',                 # tag
            {
                'to': '12345',         # 对方的 uid
                'msg': 'ba la ba la',  # 消息内容
            }
        ]

    - 消息接收方:
        ```python
        [
            'PRIVATE',                              # tag
            {
                'tm': 1437125953,                   # 时间戳
                'from': '67890',                    # 发送者 uid
                'nickname': 'Bob',                  # 昵称
                'avatar': 'http://abc.cn/xxx.png',  # 头像 URL
                'msg': 'ba la ba la'                # 消息内容
            }
        ]
        ```

### 2. 离线时聊天记录

服务器会在用户上线后，自动推送离线消息

* **tag**: HISTORY
* **data**: 消息列表, list 类型, 嵌套每一个消息体
* **示例**:

    ```python
    [
        "HISTORY",  # tag
        [
            {...},  # 离线消息 1
            {...},  # 离线消息 2
            {...},  # 离线消息 3
        ]
    ]
    ```

### 3. 系统广播推送

* **tag**: BROADCAST
* **data**: 广播内容, str 类型
* **示例**:

    ```python
    [
        'BROADCAST',  # tag
        '系统公告：吧啦吧啦吧啦。。。'
    ]
    ```

### 4. 异常

* **tag**: ERR
* **data**: 错误描述, str 类型
* **示例**:

    ```python
    [
        'ERR',
        'DataError'
    ]
    ```
