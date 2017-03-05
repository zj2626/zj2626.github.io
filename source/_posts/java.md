---
title: 1.了解java

comments: true    

tags: 
    - 深入了解java虚拟机
    - java

categories: 
    - java虚拟机

description:

date: 2017-02-05 #文章生成時間
   
---


来自<<深入了解java虚拟机>>:
Java不仅是一门编程语言, 也是一个由一系列计算机软件和规范形成的技术体系
--------------------------------------

***

##### **java技术体系包括** 
##### (这是sun公司定义的)

> 1. Java程序设计语言
> 2. 各种硬件平台上的java虚拟机
> 3. Java API类库
> 4. Class文件
> 5. 各种第三方Java类库

>其中前三部分共同统称------>JDK   (Java Development Kit)  这是支持Java程序开发的最小环境*
>JavaAPI类库中的JavaSE API子集和Java虚拟机统称------>JRE  (Java Runtime Environment) 这是支持Java程序运行的标准环境*
![这里写图片描述](http://img.blog.csdn.net/20161214190258788?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYW55YW8xMTIyMzM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

    *(这是原书上的附图)*
----------
##  *java技术体系按照业务领域目前分为4个平台**

> 1. Java Card ------> 支持Java小程序(Applets) 运行在小内存设备(智能卡)上的平台
> 2. Java ME (Micro Edition) -----> 支持Java程序运行在移动终端(手机, PDA)上的平台, 也称为J2ME
> 3. Java SE (Standard Edition) --> 支持面向桌面的级应用(如windows下的应用程序)的Java平台 提供了完整的Java核心API, 也称为J2SE
> 4. Java EE (Enterprise Edition) --> 支持使用多层架构的企业应用的Java平台, 提供了JavaSE API以及其它扩充,也称为J2EE .


----------
#### *Java发展史**
![这里写图片描述](http://img.blog.csdn.net/20161214192716089?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYW55YW8xMTIyMzM=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)

**其他大事**


 - 1999年4月,HotSpot虚拟机发布 (其原虚拟机研发公司于1997年被sun公司收购),JDK1.3以后成为所有SunJDK的默认虚拟机
 - JDK1.5以前版本语法变化较小,发布的1.5的语法层面进行了巨大改进,包括自动装箱,泛型,动态注解,foreach等,并改进了java内存模型
 - JDK1.6以后就不叫J2ME,J2SE,J2EE而改名为Java ME6, Java SE6, Java EE6
 - 2006年在JavaOne大会上 Sun公司将Java陆续开源
 - 2009年Sun公司被Oracle收购 (但Java语言由JCP组织管理)
 - 


----------
### *Java虚拟机发展史(部分)**
虚拟机版本有
 1. Sun Classic VM -->世界上第一个商用虚拟机 (JDK1.0的运行环境)
 2. Sun HotSpot VM -->目前使用范围最广的Java虚拟机 ,Sun JDK,Open JDK所带的虚拟机 :: (#当初设计               的目标是达到C语言50%以上的执行效率)
 3. KVM (Sun公司) -->简单,轻量,高度可移植,运行速度慢.广泛运用于Android,iOS等智能手机系统
 4. JRockit VM (BEA公司) -->专注服务器应用的虚拟机,所以可以不关注启动速度而运行速度快,其在垃圾回收器和MissionControl服务套件等部分的实现处于领先地位
 5. IBM J9 VM (IBM公司) --> 一款多用途虚拟机
 6. Microsoft JVM(微软) --> 这是可以说是最有意思的......当初微软也是Java技术的铁杆支持者,并且自行开发了只有win平台的java虚拟机,然而Sun公司起诉微软侵权,微软败诉于是被迫终止了Java虚拟机的研究,移除了WindowsXP中自家Java虚拟机．有趣的是当初怼人家时候说人侵权要阻止人家支持Java,真的成了之后Sun公司又到处登报纸希望Windows继续支持Java,因为那时候Sun真的是已经日薄西山了 (讽刺啊!!)


----------
#### **OpenJDK源码仓库地址***
http://hg.openjdk.java.net/jdk7u/jdk7u-dev

#### **OpenJDK官方源码包**
http://jdk7.java.net/source.html

*ps:尽量在linux或者mac上构建OpenJDK*