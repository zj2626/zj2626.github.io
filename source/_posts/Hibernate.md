---
title: Hibernate配置以及实体映射配置

comments: true    

tags: 
    - Hibernate

categories: 
    - 框架相关

description: Hibernate配置以及配置介绍 + 实体映射文件配置以及配置介绍 + 简单的创建数据库测试 

date: 2017-02-27
   
---

# **Hibernate**是一个开放源代码的对象关系映射框架，它对JDBC进行了非常轻量级的对象封装,，它将POJO与数据库表建立映射关系
# **Hibernate**是一个全自动的orm框架，hibernate可以自动生成SQL语句，自动执行，使得Java程序员可以随心所欲的使用对象编程思维来操纵数据库
---
## 下面是测试用实体1---Student.java

<!--more-->

```
package com.em.entity;

/**
 * Created by zhangjin on 2017/2/27.
 */
public class Student {
    private Integer id;
    private String name;
    private Integer age;
    private Double score;

    private Course course;

    public Student() {
    }

    public Student(String name, Integer age, Double score) {
        this.name = name;
        this.age = age;
        this.score = score;
    }

    public Student(String name, Integer age, Double score, Course course) {
        this.name = name;
        this.age = age;
        this.score = score;
        this.course = course;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Double getScore() {
        return score;
    }

    public void setScore(Double score) {
        this.score = score;
    }

    public Course getCourse() {
        return course;
    }

    public void setCourse(Course course) {
        this.course = course;
    }

    @Override
    public String toString() {
        return "Student{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", age=" + age +
                ", course=" + course +
                '}';
    }
}

```

## 其所对应的Hibernate映射文件为 Student.hbm.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-mapping PUBLIC
        "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
<!-- package:包名-->
<hibernate-mapping package="com.em.entity">
    <class name="Student" table="STUDENT">
        <!--表的主键-->
        <id name="id" type="java.lang.Integer">
            <column name="ID"/>
            <!--主键的生成方式-->
            <!--    antive:数据库本地的方式(数据库自己生成主键的方式)   increment:Hiernate以递增的方式生成(只测试时候用 因为有并发的问题)
                    identity:由底层数据库负责生成标识符(数据库必须支持主键自增) sequence:利用底层数据库提供的序列生成标识符
                    hilo:Hibernate通过高低算法生成标识符
                     -->
            <generator class="native"/>
        </id>
        <!--属性映射 name:实体属性名-->
        <!--length:限制长度 但是我测试了好几次都不起作用 无论是String还是Integer-->
        <property name="name" type="java.lang.String" length="100">
            <!--column: 数据库中列名-->
            <column name="NAME"/>
        </property>
        <property name="age" type="java.lang.Integer" length="10">
            <column name="AGE"/>
        </property>
        <!--index: 为SCORE列添加索引 索引名:score_index-->
        <property name="score" type="java.lang.Double" index="score_index">
            <column name="SCORE"/>
        </property>

        <!--映射关联关系(即外键) class:外键对应的类名 column:外键列名-->
        <many-to-one name="course" class="Course" column="COURSE_ID"/>

        <!--匿名查询使用的查询语句(可以把部分查询语句配置在配置文件中 方便修改)-->
        <query name="findByName"><![CDATA[from Student where name like :name and score > :score]]></query>
    </class>
</hibernate-mapping>
```

---
## 下面是测试用实体2---Course.java
```
package com.em.entity;

import java.sql.Timestamp;
import java.util.HashSet;
import java.util.Set;

/**
 * Created by zhangjin on 2017/2/27.
 */

public class Course {
    private Integer id;
    private String courseName;
    private Timestamp courseTime;

    Set<Student> stuSet = new HashSet<>();

    public Course() {
    }

    public Course(String courseName, Timestamp courseTime) {
        this.courseName = courseName;
        this.courseTime = courseTime;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public Timestamp getCourseTime() {
        return courseTime;
    }

    public void setCourseTime(Timestamp courseTime) {
        this.courseTime = courseTime;
    }

    public Set<Student> getStuSet() {
        return stuSet;
    }

    public void setStuSet(Set<Student> stuSet) {
        this.stuSet = stuSet;
    }

    @Override
    public String toString() {
        return "Course{" +
                "id=" + id +
                ", courseName='" + courseName + '\'' +
                ", courseTime=" + courseTime +
                '}';
    }
}

```

## 其所对应的Hibernate映射文件为 Course.hbm.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-mapping PUBLIC
        "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-mapping-3.0.dtd">
<hibernate-mapping package="com.em.entity">
    <!--
    dynamic-insert:动态插入: 设置插入只插入非空的属性(默认为false)
            设置之后insert语句只包含非空的参数,
            没有值的字段不会出现在insert语句中
    dynamic-update:动态更新: 同上,换成更新(默认false)
        动态update对性能有一个重大的影响，就是打开了以后，不同的对象的sql语句会不一样，
        如果你一次更新多条记录，hibernate将不能使用 executeBatch进行批量更新，这样效率降低很多。
        同时，在这种情况下，多条sql意味着数据库要做多次sql语句编译。
    select-before-update 设置在每次更新操作前都查询一次,(默认false)
            如果查询的数据库中数据与要更新的实体相同就不会执行更新语句,但是无论是否更新都会先执行查询,效率低
    -->
    <class name="Course" table="COURSE" dynamic-insert="true" dynamic-update="false" select-before-update="false">
        <id name="id" type="java.lang.Integer" length="10">
            <column name="ID"/>
            <generator class="native"/>
        </id>
        <property name="courseName" type="java.lang.String" length="100">
            <column name="COURSE_NAME"/>
        </property>
        <property name="courseTime" type="java.sql.Timestamp" index="time_index">
            <column name="COURSE_TIME"/>
        </property>

        <!--映射一对多的集合属性-->
        <!--属性:fetch
                select(默认): 延迟检索
                join : 迫切采用做外连接的方式初始化n关联的1的一端的属性
            属性:lazy
                proxy : 延迟检索
                false : 立即检索
            属性:inverse:设置true的一方(Set端设置)放弃维护关联关系,可减少维护次数,减少内存消耗
            属性:cascade:设置级联操作(默认none)
                -->
        <set name="stuSet" inverse="true" fetch="select">
            <key column="COURSE_ID"/><!--多的一端的数据库外键名-->
            <one-to-many class="Student"/><!--一对多对应的类-->
        </set>
    </class>
</hibernate-mapping>
```
---
## hibernate.cfg.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://hibernate.sourceforge.net/hibernate-configuration-3.0.dtd">
<hibernate-configuration>
    <session-factory>
        <!--连接数据库配置-->
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password">fangshuoit</property>
        <property name="hibernate.connection.driver_class">com.mysql.jdbc.Driver</property>
        <property name="hibernate.connection.url">jdbc:mysql://127.0.0.1:3306/test</property>

        <!--hibernate信息配置-->
        <!--hibernate使用的数据库方言-->
        <property name="hibernate.dialect">org.hibernate.dialect.MySQL57InnoDBDialect</property>
        <!--操作时是否在控制台打印sql-->
        <property name="show_sql">true</property>
        <!--是否对sql进行格式化-->
        <property name="format_sql">false</property>
        <!--指定自动生成数据表的策略-->
        <!--create:每次重新生成数据表    create-drop:每次重新生成表,SessionFactory关闭就删表
            update:每次只是更新,不改变数据    validate:不一样就抛异常,不修改表-->
        <property name="hbm2ddl.auto">update</property>
        <!--设置事务隔离级别-->
        <property name="connection.isolation">2</property>
        <!--设置删除对象后 使其OID置为null-->
        <property name="use_identifier_rollback">true</property>

        <!--c3p0连接池配置-->
        <!--连接池最大连接数-->
        <property name="c3p0.max_size">10</property>
        <!--连接池最小连接数-->
        <property name="c3p0.min_size">5</property>
        <!--连接池的连接耗尽时,一次向再获取多少个数据库连接-->
        <property name="c3p0.acquire_increment">2</property>
        <!--连接对象在多久未使用,会被销毁 2s-->
        <property name="c3p0.idle_test_period">2000</property>
        <!--多久时间检测一次连接超时情况-->
        <property name="c3p0.timeout">2000</property>
        <!--缓存Statement对象数量-->
        <property name="c3p0.max_statements">10</property>

        <!--mysql无效 oracle有效-->
        <!--设定jdbc的Statement读取数据的时候每次从数据库中取出多少记录条数-->
        <property name="jdbc.fetch_size">100</property>
        <!--设定对数据库进行批量操作(增删改)时 一次操作的条数-->
        <property name="jdbc.batch_size">50</property>

        <!--启用二级缓存-->
        <property name="cache.use_second_level_cache">true</property>
        <property name="hibernate.cache.region.factory_class">org.hibernate.cache.ehcache.EhCacheRegionFactory
        </property>
        <!--启用查询缓存-->
        <property name="cache.use_query_cache">true</property>

        <!--
                配置管理session的方式 就是配置session绑定到某一运行环境
        (将getCurrentSession()返回的session绑定到当前运行线程中 此session的上下文是thread)
        -->
        <!--注意：Spring3.x不能为thread，否则报错:org.hibernate.HibernateException: save is not valid without active transaction ，
               以上配置在 增加、删除、修改 操作时，都能正确执行，事务也正常执行！
               当执行 查询 操作时，不需要事务的支持，问题来了，报错:org.hibernate.HibernateException: No Session found for current thread
               意思是必须在transcation.isActive()条件下才能执行，
               可以解决办法是：当方法不需要事务支持的时候，使用 Session session = sessionFactory.openSession()来获得Session对象，问题解决！
                -->
        <!--<property name="current_session_context_class">thread</property>-->

        <!--指定关联的.hbm.xml文件-->
        <mapping resource="com/em/entity/Student.hbm.xml"/>
        <mapping resource="com/em/entity/Course.hbm.xml"/>

        <!--设置使用二级缓存的类(类级别的二级缓存) 以及使用二级缓存的策略usage-->
        <class-cache class="com.em.entity.Student" usage="read-write"/>
        <class-cache class="com.em.entity.Course" usage="read-write"/>
        <!--设置使用二级缓存的类(集合级别的二级缓存) 以及使用二级缓存的策略usage-->
        <collection-cache collection="com.em.entity.Course.stuSet" usage="read-write"/>
    </session-factory>

</hibernate-configuration>
```
---
# 单元测试
```
package com.em.hibernate;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import org.hibernate.service.ServiceRegistry;
import org.hibernate.service.ServiceRegistryBuilder;
import org.junit.Test;

/**
 * Created by zhangjin on 2017/2/27.
 */
public class HibernateTest {
    private static SessionFactory factory;

    static {
//        .configuere()方法中参数为hibernate.cfg.xml配置文件位置 不填写表示取src目录下
        Configuration configuration = new Configuration().configure();
        ServiceRegistry serviceRegistry = new ServiceRegistryBuilder()
                .applySettings(configuration.getProperties()).buildServiceRegistry();
        factory = configuration.buildSessionFactory(serviceRegistry);
    }
		
	private Session getSession() {
        return factory.openSession();
	}
    
    @Test
    public void test(){
        //junit运行创建数据库表以及表结构
    }
}
```
