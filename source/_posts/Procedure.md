---
title: 运用存储过程批量更新数据库中某个字段

comments: true    

tags: 
    - mysql
    - 存储过程

categories: 
    - 数据库

description: 

date: 2017-02-05 #文章生成時間
   
---

**这是目标表 **
![](http://115.159.40.33/wp-content/uploads/2017/02/1.png)
**这是来源表 **
![](http://115.159.40.33/wp-content/uploads/2017/02/2.png)
**目的:要把exam_add表中的memo字段根据idCard字段对应更新到w_secondary_score表的memo

**
```
BEGIN
    DECLARE pidCard varchar(20); /*存放idCard*/
DECLARE pmemo varchar(255);  /*存放memo*/

    declare done int default -1; 
    DECLARE cur CURSOR FOR(SELECT idCard, memo from exam_end); /*定义一个游标*/
    DECLARE continue handler for not found set done=1;  

    OPEN cur;
    myLoop: LOOP  
        FETCH cur INTO pidCard,pmemo; /*把游标内数据赋值给变量*/

        if done = 1 then   
            leave myLoop;  
          end if;  

        UPDATE w_secondary_score set memo = pmemo where idCard = pidCard; /*循环更新*/

    end loop myLoop; 
    CLOSE cur;
```
**更新成功!!!!!!**
**ps:在导入excel表到数据库的时候(通过navicat软件),出现中文乱码, 解决方案: **

**方法1.**把excel表格编码修改为与数据库相同的编码(我的是utf-8),像这样 
![](http://115.159.40.33/wp-content/uploads/2017/02/3.png)
(百度说可以, 然而我试了依然乱码) 

**方法2**:我看到navicat可以导入.txt文件 那么可以把excel先转为.txt文件设置编码为utf-8,然后再导入—–>成功!
![](http://115.159.40.33/wp-content/uploads/2017/02/4.png)
![](http://115.159.40.33/wp-content/uploads/2017/02/5.png)
![](http://115.159.40.33/wp-content/uploads/2017/02/6.png)