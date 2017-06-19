---
title: DBCP连接池介绍(转载)

comments: true    

tags: 
    - DBCP

categories: 
    - 数据库连接池

description: 

date: 2017-02-12
   
---

*文章发表时间: 2014-03-07,现在情况可能不同*   http://www.myhack58.com/Article/60/61/2014/42761.htm


 DBCP连接池介绍
 
-----------------------------
目前 DBCP 有两个版本分别是 1.3 和 1.4。
DBCP 1.3 版本需要运行于 JDK 1.4-1.5 ，支持 JDBC 3。
DBCP 1.4 版本需要运行于 JDK 1.6 ，支持 JDBC 4。
1.3和1.4基于同一套源代码，含有所有的bug修复和新特性。因此在选择DBCP版本的时候，要看你用的是什么JDK版本。
DBCP1.2版本性能一般，比c3p0差挺多。DBCP1.4和1.3，配合（依赖）commons pool 1.6的jar包,各方面功能、性能推进到新的高峰。相对1.2版本提高不少。超越(或相当)了c3p0.建议使用DBCP1.4或1.3 +  commons pool 1.6
 
Tomcat7 中保留DBCP连接池，以兼容已有应用。并提供了新的Tomcat JDBC pool作为DBCP的可选替代。新出的Tomcat JDBC pool，据说比DBCP 1.4要好，未接触，也不在本文讨论范围内。
 
DBCP连接池配置参数讲解
 
-----------------------------

<!--more-->

一、Apache官方DBCP文档给出的配置示例：
可参见：http://tomcat.apache.org/tomcat-6.0-doc/jndi-datasource-examples-howto.html

<Context>
  <Resource name="jdbc/TestDB" auth="Container" type="javax.sql.DataSource"
               maxActive="100" maxIdle="30" maxWait="10000"
               username="javauser" password="javadude" driverClassName="com.mysql.jdbc.Driver"
               url="jdbc:mysql://localhost:3306/javatest"/>
</Context>
 
 
二、常用参数说明：
可参见：http://elf8848.iteye.com/blog/337981

        <Resource
            name="jdbc/TestDB"  JNDI数据源的name
            type="javax.sql.DataSource"
        
            driverClassName="com.mysql.jdbc.Driver" JDBC驱动类
            url=""
            username="" 访问数据库用户名
            password="" 访问数据库的密码
        
            maxActive="80" 最大活动连接 //我使用版本是2.1,最大连接名称变为maxTotal
            initialSize="10"  初始化连接
            maxIdle="60"   最大空闲连接
            minIdle="10"   最小空闲连接
            maxWait="3000" 从池中取连接的最大等待时间，单位ms.
         
            validationQuery = "SELECT 1"  验证使用的SQL语句
            testWhileIdle = "true"      指明连接是否被空闲连接回收器(如果有)进行检验.如果检测失败,则连接将被从池中去除.
            testOnBorrow = "false"   借出连接时不要测试，否则很影响性能
            timeBetweenEvictionRunsMillis = "30000"  每30秒运行一次空闲连接回收器
            minEvictableIdleTimeMillis = "1800000"  池中的连接空闲30分钟后被回收
            numTestsPerEvictionRun="3" 在每次空闲连接回收器线程(如果有)运行时检查的连接数量
            
            removeAbandoned="true"  连接泄漏回收参数，当可用连接数少于3个时才执行
            removeAbandonedTimeout="180"  连接泄漏回收参数，180秒，泄露的连接可以被删除的超时值
        />
        
 
DBCP连接池的自我检测
 
-----------------------------
默认配置的DBCP连接池，是不对池中的连接做测试的，有时连接已断开了，但DBCP连接池不知道，还以为连接是好的呢。
应用从池中取出这样的连接访问数据库一定会报错。这也是好多人不喜欢DBCP的原因。
 
问题例一：
MySQL8小时问题，Mysql服务器默认连接的“wait_timeout”是8小时，也就是说一个connection空闲超过8个小时，Mysql将自动断开该 connection。
但是DBCP连接池并不知道连接已经断开了，如果程序正巧使用到这个已经断开的连接，程序就会报错误。
 
问题例二：
    以前还使用Sybase数据库，由于某种原因，数据库死了后重启、或断网后恢复。
    等了约10分钟后，DBCP连接池中的连接还都是不能使用的（断开的），访问数据应用一直报错，最后只能重启Tomcat问题才解决 。
 
解决方案：
    方案1、定时对连接做测试，测试失败就关闭连接。
    方案2、控制连接的空闲时间达到N分钟，就关闭连接，（然后可再新建连接）。
    以上两个方案使用任意一个就可以解决以述两类问题。如果只使用方案2，建议 N <= 5分钟。连接断开后最多5分钟后可恢复。
    也可混合使用两个方案，建议 N = 30分钟。
    
    下面就是DBCP连接池，同时使用了以上两个方案的配置配置
		
    validationQuery = "SELECT 1"  验证连接是否可用，使用的SQL语句
    testWhileIdle = "true"      指明连接是否被空闲连接回收器(如果有)进行检验.如果检测失败,则连接将被从池中去除.
    testOnBorrow = "false"   借出连接时不要测试，否则很影响性能
		  timeBetweenEvictionRunsMillis = "30000"  每30秒运行一次空闲连接回收器
    minEvictableIdleTimeMillis = "1800000"  池中的连接空闲30分钟后被回收,默认值就是30分钟。
    numTestsPerEvictionRun="3" 在每次空闲连接回收器线程(如果有)运行时检查的连接数量，默认值就是3.
    
    解释：
    配置timeBetweenEvictionRunsMillis = "30000"后，每30秒运行一次空闲连接回收器（独立纯种）。并每次检查3个连接，如果连接空闲时间超过30分钟就销毁。销毁连接后，连接数量就少了，如果小于minIdle数量，就新建连接，维护数量不少于minIdle，过行了新老更替。
    testWhileIdle = "true" 表示每30秒，取出3条连接，使用validationQuery = "SELECT 1" 中的SQL进行测试 ，测试不成功就销毁连接。销毁连接后，连接数量就少了，如果小于minIdle数量，就新建连接。
    testOnBorrow = "false" 一定要配置，因为它的默认值是true。false表示每次从连接池中取出连接时，不需要执行validationQuery = "SELECT 1" 中的SQL进行测试。若配置为true,对性能有非常大的影响，性能会下降7-10倍。所在一定要配置为false.
    每30秒，取出numTestsPerEvictionRun条连接（本例是3，也是默认值），发出"SELECT 1" SQL语句进行测试 ，测试过的连接不算是“被使用”了，还算是空闲的。连接空闲30分钟后会被销毁。
    
 ---
 
DBCP连接池配置参数注意事项  
 

maxIdle值与maxActive值应配置的接近。
因为，当连接数超过maxIdle值后，刚刚使用完的连接（刚刚空闲下来）会立即被销毁。而不是我想要的空闲M秒后再销毁起一个缓冲作用。这一点DBCP做的可能与你想像的不一样。
若maxIdle应与maxActive相差较大，在高负载的系统中会导致频繁的创建、销毁连接，连接数在maxIdle与maxActive间快速频繁波动，这不是我想要的。
高负载的系统的maxIdle值可以设置为与maxActive相同或设置为-1(-1表示不限制)，让连接数量在minIdle与maxIdle间缓冲慢速波动。
 
timeBetweenEvictionRunsMillis建议设置值
initialSize="5"，会在tomcat一启动时，创建5条连接，效果很理想。
但同时我们还配置了minIdle="10"，也就是说，最少要保持10条连接，那现在只有5条连接，哪什么时候再创建少的5条连接呢？
1、等业务压力上来了， DBCP就会创建新的连接。
2、配置timeBetweenEvictionRunsMillis=“时间”,DBCP会启用独立的工作线程定时检查，补上少的5条连接。销毁多余的连接也是同理。
 
 ---
 
连接销毁的逻辑
 
DBCP的连接数会在  0 - minIdle - maxIdle - maxActive  之间变化。变化的逻辑描述如下：
 
默认未配置initialSize(默认值是0)和timeBetweenEvictionRunsMillis参数时，刚启动tomcat时，连接数是0。当应用有一个并发访问数据库时DBCP创建一个连接。
目前连接数量还未达到minIdle，但DBCP也不自动创建新连接已使数量达到minIdle数量（没有一个独立的工作线程来检查和创建）。
随着应用并发访问数据库的增多，连接数也增多，但都与minIdle值无关，很快minIdle被超越，minIdle值一点用都没有。
直到连接的数量达到maxIdle值，这时的连接都是只增不减的。 再继续发展，连接数再增多并超过maxIdle时，使用完的连接（刚刚空闲下来的）会立即关闭，总体连接的数量稳定在maxIdle但不会超过maxIdle。
但活动连接（在使用中的连接）可能数量上瞬间超过maxIdle，但永远不会超过maxActive。
这时如果应用业务压力小了，访问数据库的并发少了，连接数也不会减少（没有一个独立的线程来检查和销毁），将保持在maxIdle的数量。
 
默认未配置initialSize(默认值是0)，但配置了timeBetweenEvictionRunsMillis=“30000”（30秒）参数时，刚启动tomcat时，连接数是0。马上应用有一个并发访问数据库时DBCP创建一个连接。
目前连接数量还未达到minIdle，每30秒DBCP的工作线程检查连接数是否少于minIdle数量，若少于就创建新连接直到达到minIdle数量。
随着应用并发访问数据库的增多，连接数也增多，直到达到maxIdle值。这期间每30秒DBCP的工作线程检查连接是否空闲了30分钟，若是就销毁。但此时是业务的高峰期，是不会有长达30分钟的空闲连接的，工作线程查了也是白查，但它在工作。到这里连接数量一直是呈现增长的趋势。
当连接数再增多超过maxIdle时，使用完的连接(刚刚空闲下来)会立即关闭，总体连接的数量稳定在maxIdle。停止了增长的趋势。但活动连接（在使用中的连接）可能数量上瞬间超过maxIdle，但永远不会超过maxActive。
这时如果应用业务压力小了，访问数据库的并发少了，每30秒DBCP的工作线程检查连接(默认每次查3条)是否空闲达到30分钟(这是默认值)，若连接空闲达到30分钟，就销毁连接。这时连接数减少了，呈下降趋势，将从maxIdle走向minIdle。当小于minIdle值时，则DBCP创建新连接已使数量稳定在minIdle，并进行着新老更替。
 
配置initialSize=“10”时，tomcat一启动就创建10条连接。其它同上。
 
minIdle要与timeBetweenEvictionRunsMillis配合使用才有用,单独使用minIdle不会起作用。
 
 ---
 
Tomcat中配置DBCP连接池
 
Tomcat自带DBCP的包，是$CATALINA_HOME/lib/tomcat-dbcp.jar。
omcat-dbcp.jar含有commons pool、commons DBCP两个包的内容。但只含有与连接池有关的类。
数据源配置在context.xml文件中， 要在tomcat的lib目录中放jdbc 驱动包
数据源配置在server.xml的host中，不需要在tomcat的lib目录中放jdbc 驱动包，只使用工程中的jdbc驱动包
 
 
JNDI配置:更改tomcat的server.xml或context.xml
 
    全局的数据源：
    如果需要配置全局的 Resource，则在server.xml的GlobalNamingResources节点里加入Resource，再在Context节点里加入ResourceLink的配置。
    全局的resource只是为了重用，方便所有该tomcat下的web工程的数据源管理，但如果你的tomcat不会同时加载多个web工程，也就是说一个tomcat只加载一个web工程时，是没有必要配置全局的resource的。
 
每个web工程一个数据源：
在$CATALINA_HOME/conf/context.xml的根节点Context里加入Resource配置。这种配置方法，你在context.xml配置了一个数据源，但Tomcat中有同时运行着5个工程，那了就坏事儿了，这个在Tomcat启动时数据源被创建了5份，每个工程1份数据源。连接数会是你配置的参数的5倍。
只有在你的Tomcat只加载一个web工程时,才可以直接以context.xml配置数据源。
 
        <Resource name="jdbc/testDB"       //指定的jndi名称，会用于spring数据源bean的配置和ResourceLink的配置
                       type="javax.sql.DataSource"   //数据源床型，使用标准的javax.sql.DataSource
                       driverClassName="com.mysql.jdbc.Driver"    //JDBC驱动器 
                       url="jdbc:mysql://localhost:3306/test" //数据库URL地址             
                       username="test"     //数据库用户名
                       password="test"   //数据库密码
                       maxIdle="40"   //最大的空闲连接数
                       maxWait="4000" //当池的数据库连接已经被占用的时候，最大等待时间
                       maxActive="40" //连接池当中最大的数据库连接
                       removeAbandoned="true" 
                       removeAbandonedTimeout="180"
                       logAbandoned="true" //被丢弃的数据库连接是否做记录，以便跟踪
                       factory="org.apache.tomcat.dbcp.dbcp.BasicDataSourceFactory" />
 
 

      这里的factory指的是该Resource 配置使用的是哪个数据源配置类，这里使用的是tomcat自带的标准数据源Resource配置类，这个类也可以自己写，实现javax.naming.spi.ObjectFactory 接口即可。某些地方使用的commons-dbcp.jar中的org.apache.commons.dbcp.BasicDataSourceFactory，如果使用这个就需把commons-dbcp.jar及其依赖的jar包，都放在tomcat的lib下，光放在工程的WEB-INF/lib下是不够的。
 
     ResourceLink 的配置有多种：
 
     1)tomcat安装目录下的conf/context.xml，把全局的resource直接公开给该tomcat下的所有web工程，在Context节点中加入：
<ResourceLink global="jdbc/testMDB" name="jdbc/testMDB" type="javax.sql.DataSource"/>   
不建议在此文件中，不使用<ResourceLink/>，而使用<Resource/>直接配置数据源，原因上面已说明了。   
 
     2)tomcat安装目录下的conf/server.xml，该方法可以指定把哪些source绑定到哪个web工程下。
<!-- 新增，第一行为加载的工程配置，第二行是该工程需要的ResourceLink配置 -->
<context docBase="/web/webapps/phoenix" path="" reloadable="false"> 
      <ResourceLink global="jdbc/testMDB" name="jdbc/testMDB" type="javax.sql.DataSource"/>
</context>
也可在此文件中，不使用<ResourceLink/>，而使用<Resource/>直接配置数据源。
 
     3)安装目录下的conf/localhost/下建立一个xml文件，文件名是<yourAppName>.xml。比如工程名为test，则该xml名为test.xml。
<?xml version="1.0" encoding="UTF-8"?>
<Context>   
    <ResourceLink global="jdbc/testMDB" name="jdbc/testMDB" type="javax.sql.DataSource"/>       
</context>
也可在此文件中，不使用<ResourceLink/>，而使用<Resource/>直接配置数据源。
 
     4)tomcat安装目录下的\webapps\test\META-INF\context.xml的Context节点中增加:
<ResourceLink global="jdbc/testMDB" name="jdbc/testMDB" type="javax.sql.DataSource"/>
也可在此文件中，不使用<ResourceLink/>，而使用<Resource/>直接配置数据源。
 
 
本文内容都在tomcat6.0上运行测试过，还下载了commons DBCP的源码，加入了跟踪日志，用于验证本文的理论。
