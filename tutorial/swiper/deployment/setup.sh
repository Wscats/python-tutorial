#!/bin/bash

# 系统更新
system_update() {
    echo '正在更新系统...'
    apt update -y
    apt upgrade -y
    echo -e '系统更新完毕.\n'
}


# 安装系统软件
install_software() {
    echo '正在安装系统组件...'
    BASIC='man gcc make sudo lsof ssh openssl tree vim language-pack-zh-hans'
    EXT='dnsutils iputils-ping net-tools psmisc sysstat'
    NETWORK='curl telnet traceroute wget'
    LIBS='libbz2-dev libpcre3 libpcre3-dev libreadline-dev libsqlite3-dev libssl-dev zlib1g-dev'
    SOFTWARE='git mysql-server zip p7zip apache2-utils sendmail'
    apt install -y $BASIC $EXT $NETWORK $LIBS $SOFTWARE

    echo '正在清理临时文件'
    apt autoremove
    apt autoclean

    echo '正在设置中文环境'
    locale-gen zh_CN.UTF-8
    export LC_ALL='zh_CN.utf8'
    echo "export LC_ALL='zh_CN.utf8'" >> /etc/bash.bashrc

    echo '正在启动邮件服务'
    service sendmail start

    echo -e '系统组件安装完毕.\n'
}


# 安装 Nginx
install_nginx() {
    echo '正在安装 Nginx...'
    if ! which nginx > /dev/null
    then
        wget -P /tmp 'http://nginx.org/download/nginx-1.14.1.tar.gz'
        tar -xzf /tmp/nginx-1.14.1.tar.gz -C /tmp
        cd /tmp/nginx-1.14.1
        ./configure
        make
        make install
        cd -
        rm -rf /tmp/nginx*
        ln -s /usr/local/nginx/sbin/nginx /usr/local/bin/nginx
        echo -e 'Nginx 安装完毕.\n'
    else
        echo -e 'Nginx 已存在.\n'
    fi
}


# 安装 Redis
install_redis() {
    echo '正在安装 Redis'
    if ! which redis-server > /dev/null
    then
        wget -P /tmp/ 'http://download.redis.io/releases/redis-5.0.0.tar.gz'
        tar -xzf /tmp/redis-5.0.0.tar.gz -C /tmp
        cd /tmp/redis-5.0.0
        make && make install
        cd -
        rm -rf /tmp/redis*
        echo -e 'Redis 安装完毕.\n'
    else
        echo -e 'Redis 已存在\n'
    fi
}


# 安装 pyenv
install_pyenv() {
    echo '正在安装 pyenv...'
    if ! which pyenv > /dev/null
    then
        curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
        export PATH="$HOME/.pyenv/bin:$PATH"
        eval "$(pyenv init -)"
        eval "$(pyenv virtualenv-init -)"
        echo -e 'pyenv 安装完毕.\n'
    else
        echo -e 'pyenv 已存在\n'
    fi
    pyenv update
}


# 将 pyenv 配置写入 bashrc
set_pyenv_conf() {
echo '正在配置 pyenv...'
cat >> $HOME/.bashrc << EOF

# PyenvConfig
export PATH="\$HOME/.pyenv/bin:\$PATH"
eval "\$(pyenv init -)"
eval "\$(pyenv virtualenv-init -)"
EOF

source $HOME/.bashrc
echo -e 'pyenv 配置完毕.\n'
}


# 编译安装 Python 3.6.7
install_python() {
    echo '正在安装 Python 3.6'
    if ! pyenv versions|grep 3.6.7 > /dev/null;
    then
        pyenv install -v 3.6.7
        echo -e 'Python 3.6.7 安装完毕.\n'
    else
        echo 'Python 3.6.7 已存在'
    fi
    pyenv global 3.6.7
}


# 项目环境初始化
project_init() {
    echo '正在设置项目环境...'
    proj='/opt/swiper/'
    mkdir -p $proj/{backend,frontend,deployment,data,logs}

    echo '正在创建 python 运行环境...'
    if [ ! -d $proj/.venv ]; then
        python -m venv $proj/.venv
    fi
    source $proj/.venv/bin/activate
    pip install -U pip
    if [ -f $proj/requirements.txt ]; then
        pip install -r $proj/requirements.txt
    fi
    deactivate

    echo -e '项目环境设置完毕.\n'
}

install_all() {
    system_update
    install_software
    install_nginx
    install_redis
    install_pyenv
    set_pyenv_conf
    install_python
    project_init
}


cat << EOF
请输入要执行的操作的编号: [1-9]
===============================
【 1 】 系统更新
【 2 】 安装系统组件
【 3 】 安装 Nginx
【 4 】 安装 Redis
【 5 】 安装 Pyenv
【 6 】 写入 pyenv 配置
【 7 】 安装 Python
【 8 】 项目运行环境初始化
【 9 】 全部执行
【 Q 】 退出
===============================
EOF

if [[ -n $1 ]]; then
    input=$1
    echo "执行操作: $1"
else
    read -p "请选择: " input
fi

case $input in
    1) system_update;;
    2) install_software;;
    3) install_nginx;;
    4) install_redis;;
    5) install_pyenv;;
    6) set_pyenv_conf;;
    7) install_python;;
    8) project_init;;
    9) install_all;;
    *) exit;;
esac
