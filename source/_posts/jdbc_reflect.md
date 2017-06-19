---
title: JDBC工具类-利用java反射机制

comments: true    

tags: 
    - CRUD
    - 工具类

categories: 
    - JDBC

description: 

date: 2017-02-08
   
---

1. 利用java反射机制,动态进行数据库操作
2. 可以对不同的表(对应相应的实体类)进行数据库操作而不需要修改操作代码
3. 查询得到的数据通过反射机制已经动态赋值到实体对象中

----


![](http://www.ay2626.me/wp-content/uploads/2017/02/jdbc.png)

<!--more-->

---

        package com.jdbc;
        
        import org.junit.Test;
        
        import java.io.IOException;
        import java.lang.reflect.Field;
        import java.sql.*;
        import java.util.*;
        
        /**
         * Created by zj2626 on 17-1-19.
         */
        
        public class utilsTest {
            @Test
            public void test() {<img src="http://www.ay2626.me/wp-content/uploads/2017/02/jdbc-300x115.png" alt="" width="300" height="115" class="alignnone size-medium wp-image-233" />
                /**
                 * 带占位符和别名的sql语句 查询
                 * 别名是为了匹配数据库中字段名与实体类中属性的差异(如数据库表中列f_id对应类中id属性)
                 */
                String sql = "SELECT f_id id, f_name name, f_age age FROM student WHERE f_id = ?";
        
                List<Student> list = query(Student.class, sql, 122);
                System.out.println(list != null ? "查询到的数据有" + list.size() + "条" : "没查到!!!");
            }
        
            //<T> List<T>中第一个T是泛型的声明,使T有意义,表示这是一个泛型方法
            // (即告诉人们T代表任意类型,每次只能表示一个类型)
        
            private <T> List<T> query(Class<T> clazz, String sql, Object... args) {//使用可变参数表示查询条件
                List<T> list = new ArrayList<T>(); //用来存放查询到的结果
        
                Connection connection = null;
                PreparedStatement state = null;
                ResultSet resultSet = null;
        
                try {
                    Properties properties = new Properties();
                    //读取文件中的数据库配置信息赋值给各个变量
                    properties.load(this.getClass().getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties"));
                    String dirverClass = properties.getProperty("driver");
                    String url = properties.getProperty("jdbc_url");
                    String user = properties.getProperty("user");
                    String password = properties.getProperty("password");
        
                    Class.forName(dirverClass);
                    connection = DriverManager.getConnection(url, user, password);
                    state = connection.prepareStatement(sql);
                    for (int i = 0; i < args.length; i++) {
                        state.setObject(i + 1, args[i]); //遍历设置占位符的值
                    }
        
                    /*
                      查询过程:
                      1.先利用sql语句进行查询
                      2.利用反射新建类的实体
                      3.获得sql语句中的别名,(tongg ResultSet的元数据对象--ReslutSetMetaData,其可以从结果集中获得所有信息,包括列名,别名等)
                      4.确定别名对应的属性并赋值给属性
                     */
                    resultSet = state.executeQuery();//查询并返回结果集
        
                    ResultSetMetaData metaData = resultSet.getMetaData();//得到结果集的元数据对象
                    while (resultSet.next()) {
                        //利用反射新建类的实体
                        T entity = null;
        
                        int len = metaData.getColumnCount();
                        for (int i = 0; i < len; i++) {
                            String columnName = metaData.getColumnName(i + 1);//遍历查看列名(这里并没用到)
                            String columnLabel = metaData.getColumnLabel(i + 1);//遍历获取列的别名
                            System.out.println(columnName + "--" + columnLabel);
                            Object columnValue = resultSet.getObject(columnLabel);//获取指定别名的列所对应的值
        
                            entity = clazz.newInstance();//newInstance()调用newInstance()必须有无参构造方法
        
                            //获取类的指定属性(一切皆对象,属性也是对象,都是Field类的实例)
        //                    Field field = clazz.getDeclaredField(columnLabel);//注:getField只能获得public字段
        //                    field.setAccessible(true);//设置为可访问(属性为private 不能直接赋值)
        //                    field.set(entity, columnValue);//为指定的属性赋值
        
                            //赋值方法2: 以上三行的赋值功能可以用apache提供的一个工具类实现
                            BeanUtils.setProperty(entity, columnLabel, columnValue);//该方法是通过实体中的属性的setter方法实现的
                        }
                        list.add(entity);
                    }
                } catch (SQLException | IOException | ReflectiveOperationException e) {
                    e.printStackTrace();
                } finally {
                    close(connection, state, resultSet);
                }
                return list;
            }
        
            private void close(Connection connection, PreparedStatement statement, ResultSet resultSet) {
                if (resultSet != null) {
                    try {
                        resultSet.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
                if (statement != null) {
                    try {
                        statement.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
                if (null != connection) {
                    try {
                        connection.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        
        
## 注:如果是插入一条或者多条数据可以用下面的过程获取到插入后自动生成的主键()


		   //上面是获取connection创建PreparedStatement对象
		    state.executeUpdate();		
            //获取生成的新所有主键
			//返回的resultSet中只有一列--> 列名:GENERATED_KEY
            resultSet = state.getGeneratedKeys();
            while (resultSet.next()) {
                System.out.println(resultSet.getObject(1));
            }