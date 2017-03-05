---
title: Mongodb安装与启动

comments: true    

tags: 
    - Mongodb

categories: 
    - 数据库
    - 程序安装与配置

description: Mongodb的安装,配置,启动以及部分常见问题的解决方法

date: 2017-03-1
   
---

## **MongoDB** 是一个基于分布式文件存储的数据库。由C++语言编写;是一个介于关系数据库和非关系数据库之间的产品

## 其支持的数据结构非常松散，是类似json的bson格式，因此可以存储比较复杂的数据类型。Mongo最大的特点是他支持的查询语言非常强大，其语法有点类似于面向对象的查询语言，几乎可以实现类似关系数据库单表查询的绝大部分功能，而且还支持对数据建立索引。

# 使用原理 :
>**面向集合**: 数据被分组存储在数据集中，被称为一个集合（Collection),每个集合在数据库中都有一个唯一的标识名，并且可以包含无限数目的文档 (类似于传统数据库中的 表(table))

>**模式自由**: 意味着对于存储在mongodb数据库中的文件，我们不需要知道它的任何结构定义;存储在集合中的文档，

> **键-值对的形式**:键用于唯一标识一个文档，为字符串类型，而值则可以是各种复杂的文件类型。我们称这种存储形式为BSON（Binary Serialized Document Format）

# 安装
1. 环境:CentOs6.5 64位 远程工具 xsell
2. 下载:官网下载 https://www.mongodb.com/download-center?jmp=nav#community 或者
	输入命令: > curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.0.6.tgz
	
3. 解压: > tar -zxvf mongodb-linux-x86_64-3.0.6.tgz
4. 移动到目录 mv  mongodb-linux-x86_64-3.0.6/ /usr/local/mongodb
5. 把bin目录添加到环境变量PATH中 : vim /etc/profile
	添加或修改为: export PATH="/usr/local/mongodb/bin:$PATH"
6. 配置自己的数据,日志等目录
	I.   > cd /usr/local/mongodb
	II. > mkdir data
	III. > mkdir log
	IV. > mkdir conf
	V. > cd conf
	VI. > touch mongodb.conf
	VII. > vim mongodb.conf
```
port = 27017
dbpath = data
logpath = log/mongod.log
fork = true
```

# 启动
7. 配置完毕 启动服务 
	1. 可以使用自己的配置文件中的配置 /usr/local/mongodb/bin/mongod -f /usr/local/mongodb/conf/mongodb.conf
	2. 也可以输入配置目录启动 /usr/local/mongodb/bin/mongod --dbpath=/usr/local/mongodb/data/  --port=12345  --fork --logpath=/usr/local/mongodb/log/mongodb.log
8. 启动之后 输入 > mongo 127.0.0.1:12345/admin 连接mongodb服务
	目前没有设置用户名密码 所以需要无认证启动, so先设置用户名密码
9. mongodb中用户是归属于数据库的 ,可以说是为数据库设置自己的用户,并设置权限,一般一个用户只是管理一个数据库
	(当然,可以设置一个超级管理员用来管理所有的数据库)
	*下面的意思是为admin数据库设置一个用户名为"root",密码为"root"的用户,用户权限(角色) 是root(超级管理员)*
```
> use admin
> db.createUser(
...   {
...     user: "root",
...     pwd: "root",
...     roles: [ { role: "root", db: "admin" } ]
...   }
... )
```
*上面是mongodb3.0的新建用户方式, 2.x的方式有所不同,自行查阅*

下面是mongodb内置的角色
```
    1. 数据库用户角色：read、readWrite;
    2. 数据库管理角色：dbAdmin、dbOwner、userAdmin；
    3. 集群管理角色：clusterAdmin、clusterManager、clusterMonitor、hostManager；
    4. 备份恢复角色：backup、restore；
    5. 所有数据库角色：readAnyDatabase、readWriteAnyDatabase、userAdminAnyDatabase、dbAdminAnyDatabase
    6. 超级用户角色：root  
    // 这里还有几个角色间接或直接提供了系统超级用户的访问（dbOwner 、userAdmin、userAdminAnyDatabase）
    7. 内部角色：__system
	
Read：允许用户读取指定数据库
readWrite：允许用户读写指定数据库
dbAdmin：允许用户在指定数据库中执行管理函数，如索引创建、删除，查看统计或访问system.profile
userAdmin：允许用户向system.users集合写入，可以找指定数据库里创建、删除和管理用户
clusterAdmin：只在admin数据库中可用，赋予用户所有分片和复制集相关函数的管理权限。
readAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读权限
readWriteAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的读写权限
userAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的userAdmin权限
dbAdminAnyDatabase：只在admin数据库中可用，赋予用户所有数据库的dbAdmin权限。
root：只在admin数据库中可用。超级账号，超级权限
```
*可以添加几个其他角色的用户来测试权限*

10. 要用用户登录的服务 so先关闭服务: > db.shutdownServer()

11. 启动带权限验证的mongodb服务: 
```
> /usr/local/mongodb/bin/mongod --dbpath=/usr/local/mongodb/data/  --port=12345  --fork --logpath=/usr/local/mongodb/log/mongodb.log -auth
```
	如果报错too many positional options是由于--的原因,需要写英文的两个-
12. 连接 > mongo 127.0.0.1:12345/admin
13. 使用数据库 use admin
14. 进行一些数据库操作 比如 > show dbs 此时就会报错 用用户名密码验证权限
```
> db.auth('root','anyao112233')
```
	返回1表示成功 返回0表示失败 ; 此时再输入:
```
> show dbs
> show collections
```
	就会返回正常结果;


# 常见问题解决
##### *注意* : > use test   //用来切换别的数据库
#####  此时如果登录的用户没有操作此数据库的权限 show dbs就会报错

	#####*注意* : 此时关闭服务>  db.shutdownServer() 可能会报错,它提示没有shutdown的权限
		解决方法: > db.grantRolesToUser( "root" , [ { role: "hostManager", db: "admin" } ])

	为用户root赋予hostManager角色的权限,然后就可以关闭了
	
15. 输入> exit 退出界面

	*注*:可以用浏览器访问 127.0.0.1:27017
	*注*:有时候shutdown以后 无法再启动 报错
		原因:1. mongodb没有正常关闭 
				解决方法:删除mongodb的data目录下的mongod.lock (不能解决就把log目录中日志删除)
			 2.上面试了还是无法启动,那就是mongodb服务可能没有访问data,log等目录的权限
			 	解决方法:> chmod -R 777 /usr/local/mongodb/



















