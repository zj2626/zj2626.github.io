---
title: Mongodb的CURD等操作

comments: true    

tags: 
    - Mongodb
    - CRUD

categories: 
    - 数据库

description: Mongodb的增删改查,索引操作

date: 2017-03-1
   
---

## 对数据库的操作
```
>show dbs   显示所有数据库
>use admin 切换数据库(数据库可以自动新建)
>db.auth('username','password') 验证用户权限
>db.dropDatabase() 删除数据库
```

## 对集合(collection)的操作(也就是对表的操作)
```
>db.集合名.drop() 删除表
>show collections 显示所有的collection
>show tables  显示所有的collection

```


## 对数据的操作

### 查询
```
>db.集合名.find()  	查询数据库中某个集合的数据
>db.集合名.find({x:1})  	查询数据库 查询包含参数json字符串的数据
>db.集合名.find().count()  	查询数据库中数据的个数(可带参数 表条件)
>db.集合名.find().skip(5).limit(10).sort({x:1,y:1})		查询条件:skip:跳过数据的个数;limit:查询条数;sort:按照某个字段排序(这里是先按x排序,再按y排序, 1表示正像排序,-1代表反向)
>
```
### 增加
```
>db.集合名.insert({x:1}) 	插入数据(参数格式为json格式,集合名可以自动新建) 插入时会自动生成id(名叫"_id"的字段)
>db.集合名.insert({x:1_id:1}) 	带id的插入(需要保证_id全局唯一,不可重复)
>for(i=0;i<100;i++) 	db.集合名.insert({x:i+200}) 使用循环插入数据库
```
### 更新
```
Update有4个参数：(默认更新一条数据)
		第一个selector(查询条件)，
		第二个newValue(要更新的数据)， $set、$inc、$push
		第三个upserts， true:查到就更新,没查到就新建
		第四个multipleUpdate,  true:批量更新
```

```
> db.集合名.update({x:10},{x:100})		更新方法: 第一个json:更新条件 ;第二个json:更新结果 (把x=1的数据更新为x=10)
> db.集合名.update({x:10},$set:{y:100}})	部分更新: 只更新第二个json所改变的字段(不加set操作符,会把原来的所有的字段覆盖为更新结果)
> db.集合名.update({x:10},{x:100}, true)  更新或插入: 如果更新的数据不存在就插入一条数据(upsert = true)
> db.集合名.update({x:10},$set:{y:100}}, false, true) 批量更新: 为防止误操作,必须使用set操作,(upsert = false,)
```

### 删除
```
(默认删除查到的所有数据)
> db.集合名.remove({x:200}) 删除操作:必须有参数

```

## 索引

### 查看索引
```
>db.collection.getIndexes()     //每个collection都会创建默认的一个索引 _id
```

### 创建索引
```
>db.collection.ensureIndex({x:1})  1表示正像排序,-1代表反向 (最好在存在大量数据之前就已经添加好索引)
```