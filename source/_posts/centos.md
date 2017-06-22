---
title: Centos下用yum安装mysql5.6

comments: true    

tags: mysql

categories: 
    - 数据库

description:  转载的,最简单的centos装mysql的教程

date: 2017-02-05 #文章生成時間
   
---

    1. 输入命令 查看当前安装的mysql:  rpm -qa | grep mysql
    2. 如果有 卸载:    rpm -e mysql　　// 普通删除模式
                      rpm -e --nodeps mysql　　// 强力删除模式，如果使用上面命令删除时，提示有依赖的其它文件，则用该命令可以对其进行强力删除
                      
    3. 查看yum上提供的mysql版本信息 : yum list | grep mysql
    
    4.安装 :    yum install -y mysql-server mysql mysql-devel

  
        在CentOS7下安装mysql 可能会提示“No package mysql-server available.”
        
        解决办法: rpm -Uvh http://dev.mysql.com/get/mysql-community-release-el7-5.noarch.rpm
                然后再安装 mysql-server
  
    
    5.查看安装好的mysql信息: rpm -qi mysql-server
    
    
    6.启动:  service mysqld start
    
    
    7. 设置密码: mysql -u root 进入mysql界面
                SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');
                
    8. 新建新用户,用于远程连接(也可以修改root用户访问权限)
                CREATE USER 'username'@'host' IDENTIFIED BY 'password'; 
                
                * username - 你将创建的用户名, 
                * host - 指定该用户在哪个主机上可以登陆,如果是本地用户可用localhost, 如果想让该用户可以从任意远程主机登陆,可以使用通配符%. 
                * password - 该用户的登陆密码,密码可以为空,如果为空则该用户可以不需要密码登陆服务器
                
                
    9. 为用户授权: GRANT privileges ON databasename.tablename TO 'username'@'host' 
    
                * privileges - 用户的操作权限,如SELECT , INSERT , UPDATE 等(详细列表见该文最后面).如果要授予所的权限则使用ALL.;
                * databasename - 数据库名,
                * tablename-表名,如果要授予该用户对所有数据库和表的相应操作权限则可用*表示, 如*.*. 

    10.设置密码: SET PASSWORD FOR 'username'@'host' = PASSWORD('newpassword');