---
title: Mybatis配置文件参考

comments: true    

tags: 
    - Mybatis

categories: 
    - 框架相关

description: Mybatis配置介绍... ps:学的时候精神不佳 

date: 2017-02-28
   
---

# Student.java

<!--more-->

```
package com.mybatis;

import java.io.Serializable;

/**
 * Created by zhangjin on 2017/2/27.
 */
public class Student implements Serializable{
    private Integer sId;
    private String name;
    private Integer sAge;
    private Double score;

    private Course course;

    public Student() {
    }

    public Student(String name, Integer sAge, Double score) {
        this.name = name;
        this.sAge = sAge;
        this.score = score;
    }

    public Student(String name, Integer sAge, Double score, Course course) {
        this.name = name;
        this.sAge = sAge;
        this.score = score;
        this.course = course;
    }

    public Integer getsId() {
        return sId;
    }

    public void setsId(Integer sId) {
        this.sId = sId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getsAge() {
        return sAge;
    }

    public void setsAge(Integer sAge) {
        this.sAge = sAge;
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
                "sId=" + sId +
                ", name='" + name + '\'' +
                ", sAge=" + sAge +
                '}';
    }
}

``` 

## 对应的映射文件(并不能像Hibernate一样可以生成数据库) com/mybatis/StudentMapper.xml


```
        <?xml version="1.0" encoding="UTF-8" ?>
        <!DOCTYPE mapper
                PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
                "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
        
        <mapper namespace="com.mybatis.StudentMapper">
            <!--开启二级缓存 : 映射文件级别的缓存(每个文件对应一个缓存)-->
            <!--
                eviction 缓存回收策略
                flushInterval:刷新间隔时间
                size:可缓存对象个数
            -->
            <cache
                    eviction="FIFO"
                    flushInterval="60000"
                    size="512"
                    readOnly="true"
            >
            </cache>
        
            <!--根据id查询得到对象-->
            <!--parameterType:参数类型  resultType:返回值类型-->
            <select id="getStudent" parameterType="int" resultType="Student">
                select * from student where id = #{sId}
            </select>
        
            <select id="getStudent2" parameterType="int" resultType="Student">
                select id sId,name name,age sAge,score name,course_id course from student where id = #{sId}
            </select>
        
            <!--CRUD-->
            <insert id="addStu" parameterType="Student">/*下面占位符写法为实体的属性名*/
                insert into student (name,age,score) values(#{name}, #{sAge}, #{score})
            </insert>
        
            <update id="updateStu" parameterType="Student">
                update student set name=#{name},age=#{sAge},score=#{score} where id=#{sId}
            </update>
        
            <delete id="delStu" parameterType="int">
                delete from student where id = #{sId}
            </delete>
        
            <select id="getStu" resultType="Student">
                select * from student
            </select>
        
            <select id="getStuWithCourse" parameterType="int" resultMap="stuMap">
                select * from student ss, course cc where ss.id = #{sId} and ss.course_id = cc.id
            </select>
        
            <!--封装键值对(映射关系)-->
            <resultMap id="stuMap" type="Student">
                <id property="sId" column="id"/>
                <result property="name" column="name"/>
                <result property="sAge" column="age"/>
                <association property="course" javaType="Course">
                    <id property="id" column="id"/>
                    <result property="courseName" column="course_name"/>
                    <result property="courseTime" column="course_time"/>
                </association>
            </resultMap>
        
        
            <select id="getStuFirst" parameterType="int" resultMap="stuMapFirst">
                select * from student where id = #{sId}
            </select>
        
            <resultMap id="stuMapFirst" type="Student">
                <id property="sId" column="id"/>
                <result property="name" column="name"/>
                <result property="sAge" column="age"/>
                <!--把第一个查询得到的course对应的course_id值传给 查询getCourseSecond-->
                <association property="course" column="course_id" select="com.mybatis.CourseMapper.getCourseFirst"/>
                <!--<association property="course" column="course_id" select="com.mybatis.CourseMapper.getCourseSecond"/>-->
            </resultMap>
        
            <select id="getStudentsByCourse" parameterType="int" resultMap="stuMap">
                select * from student ss where ss.course_id = #{id}
            </select>
        
            <!--<select id="getByScope" parameterMap="scoreMap">
                select * from student s where s.name
                <if test='name != "%null%"'>
                    like #{name} and
                </if>
                sAge between #{minAge} and #{maxAge}
            </select>
        
            <parameterMap id="scoreMap" type="">
                <!&ndash;很方&ndash;>
            </parameterMap>-->
        </mapper>
```

---

## Course.java


```
    package com.mybatis;
    
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
    
        private Set<Student> stuSet = new HashSet<>();
    
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
                    ", stuSet=" + stuSet +
                    '}';
        }
    }

```


## 对应的映射文件  com/mybatis/CourseMapper.xml

```
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE mapper
            PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
            "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
    
    <mapper namespace="com.mybatis.CourseMapper">
        <select id="getCourseFirst" parameterType="int" resultType="Course">
            select id id, course_name courseName, course_time courseTime from course where id = #{id}
        </select>
    
        <select id="getCourseSecond" parameterType="int" resultMap="couMap">
            select id id, course_name courseName, course_time courseTime from course where id = #{id}
        </select>
    
        <resultMap id="couMap" type="Course">
            <id property="id" column="id"/>
            <result property="courseName" column="course_name"/>
            <result property="courseTime" column="course_time"/>
        </resultMap>
    
        <!--select * from course cc,student ss where cc.id = ss.course_id and cc.id = #{id}-->
        <select id="getCourseWithStudents" parameterType="int" resultMap="courseWithStudentsMap">
            select * from student ss, course cc where cc.id = ss.course_id and cc.id = #{id}
        </select>
    
        <resultMap id="courseWithStudentsMap" type="Course">
            <id property="id" column="id"/>
            <result property="courseName" column="course_name"/>
            <result property="courseTime" column="course_time"/>
            <collection property="stuSet" ofType="Student">
                <id property="sId" column="id"/>
                <result property="name" column="name"/>
                <result property="sAge" column="age"/>
            </collection>
        </resultMap>
    
        <select id="getCourseWithStudents2" parameterType="int" resultMap="courseWithStudentsMap2">
            select * from course where id = #{id}
        </select>
    
        <resultMap id="courseWithStudentsMap2" type="Course">
            <id property="id" column="id"/>
            <result property="courseName" column="course_name"/>
            <result property="courseTime" column="course_time"/>
            <collection property="stuSet" column="id" select="com.mybatis.StudentMapper.getStudentsByCourse"/>
        </resultMap>
    
    </mapper>
```

---


##  数据库配置文件 com/mybatis/dataBase.properties

```
    com/mybatis/dataBase.properties
```


## Mybatis配置文件 com/mybatis/mybatis-config.xml

```
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE configuration
            PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
            "http://mybatis.org/dtd/mybatis-3-config.dtd">
    <configuration>
    
        <!--引用外部文件配置数据库-->
        <properties resource="com/mybatis/dataBase.properties"/>
    
        <!--为实体类起别名-->
        <typeAliases>
            <package name="com.mybatis" />
            <!--<typeAlias type="com.mybatis.Student" alias="_STU"/>-->
        </typeAliases>
    
        <!--
            development:开发模式
            work: 工作模式
        -->
        <environments default="development">
            <environment id="development">
                <!--事务管理器类型
                    JDBC:使用JDBC的提交和回滚
                    MANAGED:由其他容器来管理事务的生命周期
                -->
                <transactionManager type="JDBC"/>
                <!--数据源
                        UNPOOLED:使用简单的打开关闭连接
                        POOLED:使用数据库连接池管理
                -->
                <dataSource type="POOLED">
                    <property name="driver" value="${driver}"/>
                    <property name="url"
                              value="${url}?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=UTF-8"/>
                    <property name="username" value="${user}"/>
                    <property name="password" value="${password}"/>
                </dataSource>
            </environment>
        </environments>
    
        <!-- mapper 文件路径配置 -->
        <mappers>
            <mapper resource="com/mybatis/StudentMapper.xml"/>
            <mapper resource="com/mybatis/CourseMapper.xml"/>
            <mapper class="com.mybatis.StudentMapperInterface"/>
        </mappers>
    </configuration>
```

---


## 测试用类


```
    package com.mybatis;
    
    import org.apache.ibatis.session.SqlSession;
    import org.apache.ibatis.session.SqlSessionFactory;
    import org.apache.ibatis.session.SqlSessionFactoryBuilder;
    import org.junit.Test;
    
    import java.io.*;
    import java.util.Arrays;
    import java.util.List;
    
    /**
     * Created by zhangjin on 2017/2/27.
     */
    public class MyTest {
        private static SqlSessionFactory sessionFactory;
    
        {
            InputStream input = this.getClass().getClassLoader()
                    .getResourceAsStream("com/mybatis/mybatis-config.xml");
            sessionFactory = new SqlSessionFactoryBuilder().build(input);
        }
    
        @Test
        public void select() {
            SqlSession session = sessionFactory.openSession();
            String statement = "com.mybatis.StudentMapper.getStudent2";
            Student student = session.selectOne(statement, 4);
            System.out.println(student.toString());
        }
    
        @Test
        public void select2() {
            SqlSession session = sessionFactory.openSession();
            StudentMapperInterface mapper = session.getMapper(StudentMapperInterface.class);
            Student student = mapper.getById(4);
            System.out.println(student.toString());
        }
    
        @Test
        public void save() {
            SqlSession session = sessionFactory.openSession();//设置true自动提交 也可以手动提交session.commit();
            String statement = "com.mybatis.StudentMapper.addStu";
            Student student = new Student("HHd DD 的", 123, 654.456);
            int i = session.insert(statement, student);
            session.commit();
            System.out.println(i);
        }
    
        @Test
        public void save2() {
            SqlSession session = sessionFactory.openSession(true);
            StudentMapperInterface mapper = session.getMapper(StudentMapperInterface.class);
            Student student = new Student("HHdAAAAAAAAAA", 123, 654.456);
            mapper.aStu(student);
        }
    
        @Test
        public void delete() {
            SqlSession session = sessionFactory.openSession(true);
            String statement = "com.mybatis.StudentMapper.delStu";
            int i = session.delete(statement, 42);
            System.out.println(i);
        }
    
        @Test
        public void update() {
            SqlSession session = sessionFactory.openSession(true);
            String statement = "com.mybatis.StudentMapper.updateStu";
            Student student = new Student("AGCCCC", 999, 654.456);
            student.setsId(27);
    
            int i = session.update(statement, student);
            System.out.println(i);
        }
    
        @Test
        public void find() {
            SqlSession session = sessionFactory.openSession(true);
            String statement = "com.mybatis.StudentMapper.getStu";
            List<Student> stu = session.selectList(statement);
            System.out.println(stu.size());
        }
    
        @Test
        public void find2() {
            SqlSession session = sessionFactory.openSession();
            String statement = "com.mybatis.StudentMapper.getStuWithCourse";
            Student stu = session.selectOne(statement, 4);
            System.out.println(stu.toString());
        }
    
        @Test
        public void find3() {
            SqlSession session = sessionFactory.openSession();
            String statement = "com.mybatis.StudentMapper.getStuFirst";
            Student stu = session.selectOne(statement, 4);
            System.out.println(stu.toString());
        }
    
        @Test
        public void find4() {
            SqlSession session = sessionFactory.openSession();
            String statement = "com.mybatis.CourseMapper.getCourseWithStudents";
            List<Course> courseList = session.selectList(statement, 4);
            System.out.println(Arrays.toString(courseList.toArray()));
        }
    
        @Test
        public void find5() {
            SqlSession session = sessionFactory.openSession();
            String statement = "com.mybatis.CourseMapper.getCourseWithStudents2";
            List<Course> courseList = session.selectList(statement, 4);
            System.out.println(Arrays.toString(courseList.toArray()));
        }
    
        @Test
        public void testChche() {
            SqlSession session = sessionFactory.openSession();
            String statement = "com.mybatis.StudentMapper.getStudent2";
            Student student = session.selectOne(statement, 4);
            System.out.println(student.toString());
            Student student2 = session.selectOne(statement, 4);
            System.out.println(student2.toString());
            session.clearCache();
            Student student3 = session.selectOne(statement, 4);
            System.out.println(student3.toString());
            session.close();
            session = sessionFactory.openSession();
            Student student4 = session.selectOne(statement, 4);
            System.out.println(student4.toString());
            session.close();
        }
    
        @Test
        public void test(){
            try{
                int a = 10 / 0;
            }catch (Exception e){
                e.printStackTrace();
            }
    
        }
    }

```