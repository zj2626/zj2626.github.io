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
>db.集合名.find({y:{$exists:true}})  //查询y字段存在的数据
```

### 增加
```
>db.集合名.insert({x:1}) 	插入数据(参数格式为json格式,集合名可以自动新建) 插入时会自动生成id(名叫"_id"的字段)
>db.集合名.insert({x:1, _id:1}) 	带id的插入(需要保证_id全局唯一,不可重复)
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

>db.collection.ensureIndex({x:1},{name:""my_index})  自定义命名索引名

```

### 删除索引
```
>db.collection.dropIndex("index_name")  //参数是索引名
```

### 索引类型 
    1. _id索引(默认的唯一索引)
    2.单键索引: 普通索引(值为一个字符串,数字,日期等) db.collection.ensureIndex({x:1})
    3.多键索引: 当索引的字段为数组时，创建出的索引称为多key索引
```
    如果存在一个多值的字段如: { "_id" : ObjectId("58bbcfeb48e281d3bc2a95b9"), "x" : [ 1, 2, 3, 4, 5, 6 ] }
    那么在这条记录创建时候 会自动建立多键索引(或手动创建 db.collection.createIndex( {x: 1} )  )
    查询: db.collection.find({x: 1}) 或者  db.collection.find({x: 3})
```
    4.复合索引: 相当于多个单键索引 创建方式: db.collection.ensureIndex({x:1,y:1})
    5.过期索引: (TTL) 一段时间后会过期(删除数据)的索引 (过期时间 单位是秒)
        创建方式: db.collection.ensureIndex({x:1},{expireAfterSeconds:10})
        注意:   1.存储在过期索引字段的值必须是ISODate或ISODate数组,不能是其他,否则无法删除
                2.如果是Date数组就按照时间从小到大删
                3.不能是复合索引
                4.删除不是准时的,而是60s的一个定时进程执行的删除
                5.全文索引
                    db.collection.ensureIndex({"key":"text"})
                    db.collection.ensureIndex({"key":"text","key2":"text"})
                    db.collection.ensureIndex({"$**":"text"})
*其中key表示原来的"字段名",键; text表示的不是原来的正序或倒序,而是要检索的内容(创建索引要写"text")*
*一个collection只能创建一个全文索引*

```
    全文索引测试:
        创建内容:   > db.test.insert({"x":"aaa ccc"})
                   > db.test.insert({"x":"bbb"})
                   > db.test.insert({"y":"ccc"})
                   > db.test.insert({"z":"ccc"})
                   > db.test.insert({"x":"aaa111"})
                   > db.test.insert({"y":"aaa111"})
                   > db.test.insert({"x":"aaa222","y":"ccc"})
        查看创建的内容:  db.test.find()   //6条
        创建索引:   db.test.ensureIndex({"x":"text"})
        查看所有索引:db.test.getIndexes()    //2个,第一个是默认的索引
        查询:       
                    > db.test.find({$text:{$search:"aaa"}})           //没找到数据
                    
                    > db.test.find({$text:{$search:"aaa111"}})        //查到一条(全部匹配)
                    { "_id" : ObjectId("58bcb92118bc95b8f476def1"), "x" : "aaa111" }
                    
                    > db.test.find({$text:{$search:"ccc"}})
                    { "_id" : ObjectId("58bf535ae830c0c5f89055e7"), "x" : "aaa ccc" }
                    
                    > db.test.find({$text:{$search:"aaa111 aaa"}})    //或查询 用户空格分开
                    { "_id" : ObjectId("58bf535ae830c0c5f89055e7"), "x" : "aaa ccc" }
                    { "_id" : ObjectId("58bcb92118bc95b8f476def1"), "x" : "aaa111" }
                    
                    > db.test.find({$text:{$search:"aaa111 aaa -ccc"}})  //或查询,其中'-'表示不包含 
                    { "_id" : ObjectId("58bcb92118bc95b8f476def1"), "x" : "aaa111" }

                    > db.test.find({$text:{$search:"\"aaa\" \"aaa111\""}}) //与查询 1条
                    > db.test.find({$text:{$search:"\"aaa222\""}})          //1条
                    > db.test.find({$text:{$search:"\"aaa\" \"aa\""}})      //1条
                    > db.test.find({$text:{$search:"\"aaa\" \"aa\""}})      //1条
                    > db.test.find({$text:{$search:"\"aaa222\" \"aa\""}})   //1条
```

                *全文索引相似度查询 返回查询到的结果与要查询的数据的相似度
                    {score:{$meta:"textScore"}}   得到的数越大表示相似度越高
                    
```
                    > db.test.find({$text:{$search:"aaa222"}},{score:{$meta:"textScore"}})
                    { "_id" : ObjectId("58bcb92518bc95b8f476def2"), "x" : "aaa222", "y" : "ccc", "score" : 1.1 }
                    > db.test.find({$text:{$search:"aaa"}},{score:{$meta:"textScore"}})
                    { "_id" : ObjectId("58bf535ae830c0c5f89055e7"), "x" : "aaa ccc", "score" : 0.75 }
                    
                    //用相似度排序
                    > db.test.find({$text:{$search:"bbb"}},{score:{$meta:"textScore"}}).sort({score:{$meta:"textScore"}})

```
                全文索引限制:
                    1.一次只能指定一个$text查询
                    2.$text不能使用$nor查询
                    3.查询中包含$text,则hint(强制指定索引)无效
                    4.目前已经支持中文查询(版本3.0.6)

                6.地理位置索引 
                
                
### 索引属性
    1.name:   db.collection.ensureIndex({x:1},{name:"my_index"}) 指定索引名称
    2.unique: db.collection.ensureIndex({y:1},{unique:true})  设置为true,则不允许在同一个collection中插入有相同唯一索引的字段(索引的数值不能重复)
        注意:如果插入的数据没有指定的索引字段,则只能插入一条这样的数据,再插入则会报错(相当于重复)
    3.sparse: db.collection.ensureIndex({y:1},{sparse:true})  设置为true,则不会在没有的字段的数据上创建索引
            > db.collection.find({y:{$exists:true}})  //查询y字段存在的数据
```
        测试: 先插入6条数据,其中1条包含有y字段 
            > db.test3.ensureIndex({y:1},{name:"mytest_y"},{sparse:false})  //创建索引
            > db.test3.find({y:{$exists:false}})   //查询不存在y的数据 5条(数据库并没有为这5条数据建立y的索引,而是数据库优化的结果,这里查询并没有用上面的索引,so查到了)
            { "_id" : ObjectId("58bf69ced52555dec4840312"), "x" : 1 }
            { "_id" : ObjectId("58bf6c00d52555dec4840319"), "x" : 2111313, "k" : 1 }
            { "_id" : ObjectId("58bf6c13d52555dec484031a"), "x" : 2111313, "k" : 2 }
            { "_id" : ObjectId("58bf6c15d52555dec484031b"), "x" : 2111313, "k" : 3 }
            { "_id" : ObjectId("58bf6c19d52555dec484031c"), "x" : 2111313, "z" : 3 }
            > db.test3.find({y:{$exists:false}}).hint("mytest_y")     //强制指定索引,使用指定的索引查询,就无法查到不包含y的数据
            >                                                         //没有查到数据
```
    4.expireAfterSeconds 是否定时删除TTL(过期索引) 
            > db.collection.ensureIndex({x:1},{expireAfterSeconds:10})