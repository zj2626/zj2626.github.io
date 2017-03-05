---
title: Centos安装mysql5.6

comments: true    

tags: mysql

categories: 
    - Linux
    - 数据库

description:  转载的,最简单的centos装mysql的教程

date: 2017-02-05 #文章生成時間
   
---


1 创建<a class="replace_word" title="MySQL知识库" href="http://lib.csdn.net/base/mysql" target="_blank">MySQL</a>用户组和用户
<pre>groupadd mysql 
useradd -g mysql -d /sbin/nologin mysql</pre>
2 下载mysql
官网下载
<a href="https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.35-linux-glibc2.5-x86_64.tar.gz">https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.35-linux-glibc2.5-x86_64.tar.gz</a>

3 解压mysql
<pre>tar zxvf mysql-5.6.14-<a class="replace_word" title="Linux知识库" href="http://lib.csdn.net/base/linux" target="_blank">Linux</a>-glibc2.5-i686.tar.gz

mkdir /usr/local/mysql

mv mysql-5.6.14-linux-glibc2.5-i686/* /usr/local/mysql</pre>
4 初始化mysql
<pre>/usr/local/mysql/scripts/mysql_install_db –user=mysql</pre>
4 cp /usr/local/mysql/support-files/mysql.server /etc/init.d/mysqld
添加mysql到服务开机启动
<pre>chkconfig –add mysqld 
chkconfig –level 2345 mysqld on

service mysqld start</pre>
5 添加PATH
<pre>vim /etc/profile 
添加 export PATH=”/usr/local/mysql/bin:$PATH”</pre>
保存，退出，然后运行：
<pre id="source-etcprofile">source /etc/profile</pre>
6
<pre>mysql -u root -p</pre>
报错 提示 ERROR 2002 (HY000): Can’t connect to local MySQL server through socket ‘/tmp/mysql.sock’ (1)

执行
<pre>ln -s /var/lib/mysql/mysql.sock /tmp/mysql.sock</pre>