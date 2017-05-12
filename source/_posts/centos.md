---
title: Centos下用rpm安装mysql5.6

comments: true    

tags: mysql

categories: 
    - Linux
    - 数据库

description:  转载的,最简单的centos装mysql的教程

date: 2017-02-05 #文章生成時間
   
---

    1. 输入命令 查看当前安装的mysql:  rpm -qa | grep mysql
    2. 如果有 卸载:    rpm -e mysql　　// 普通删除模式
                      rpm -e --nodeps mysql　　// 强力删除模式，如果使用上面命令删除时，提示有依赖的其它文件，则用该命令可以对其进行强力删除
                      
    3. 查看yum上提供的mysql版本信息 : yum list | grep mysql
    
    4.安装 :    yum install -y mysql-server mysql mysql-devel
    5.查看安装好的mysql信息: rpm -qi mysql-server
    6.启动:  service mysqld start
