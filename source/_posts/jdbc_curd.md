---
title: 重新学习JDBC之获取连接

comments: true    

tags: 
    - CRUD
    - 工具类

categories: 
    - JDBC

description: 

date: 2017-02-07
   
---

```
package com.jdbc;

import org.apache.commons.collections.map.HashedMap;
import org.junit.Test;

import java.io.IOException;
import java.sql.*;
import java.util.*;

/**
 * Created by zj2626 on 17-1-19.
 */
public class testUtils {
    private static Connection connection = null;
    private static PreparedStatement state = null;
    private static ResultSet resultSet = null;

    @Test
    public void test() {
        Integer id = 123;
        String name = "name";
        Integer age = 20;

        List<Object> list = new ArrayList<>();
        list.add(id);
        list.add(name);
        list.add(age);

        //操作数据库版本一
        String sql = "insert into student(id, name, age) values(" + id + ", '" + name + "', " + age + ")";
        editWayOne(sql);

        //操作数据库版本二(可以防止sql注入)
        String sql2 = "insert into student(id, name, age) values(?, ?, ?)";
        //editWayTwo(sql2, list);

        //查询
        String sql3 = "select id, name, age from student where id = ?";
        query(sql3, id);
    }

    /**
     * low版本的增删改方法 (增删改都可用)
     *
     * @param sql 普通sql语句
     * @return 执行成功的记录的条数
     */
    private int editWayOne(String sql) {
        int num = 0;
        try {
            getConnection(sql);
            num = state.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
        return num;
    }

    /**
     * @param sql  带占位符的sql语句
     * @param list 占位符要传入的值
     * @return 执行成功的记录的条数
     */
    private int editWayTwo(String sql, List<Object> list) {
        int num = 0;
        try {
            getConnection(sql);
            for (int i = 0; i < list.size(); i++) {
                //这里统一用setObject了 其实应该用相对应类型的方法(setString,setInt,setDate...)
                state.setObject(i + 1, list.get(i));
            }
            num = state.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }
        return num;
    }

    /**
     * 查询
     *
     * @param sql 查询语句
     * @return 返回查询到的所有数据集合
     */
    private List<Map<String, Object>> query(String sql, Integer id) {
        List<Map<String, Object>> result = new ArrayList<>();
        try {
            getConnection(sql);
            state.setObject(1, id);
            //结果集(ResultSet)是数据中查询结果返回的一种对象 该对象存储了查询出的数据需要遍历取出
            resultSet = state.executeQuery();

            while (resultSet.next()) {//查看有没有下一条数据
                Map<String, Object> map = new HashMap();//存放每条数据的每个查询到的字段
                map.put("id", resultSet.getInt(1));//遍历也可以通过resultSet.getInt("id")更明确
                map.put("name", resultSet.getString(2));
                map.put("age", resultSet.getInt(3));

                result.add(map);
            }

            System.out.println("数据条数" + result.size());
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close();
        }

        return result;
    }

    private void getConnection(String sql) {
        Properties properties = new Properties();
        try {
            properties.load(this.getClass().getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties"));
        } catch (IOException e) {
            e.printStackTrace();
        }

        String dirverClass = properties.getProperty("driver");
        String url = properties.getProperty("jdbc_url");
        String user = properties.getProperty("user");
        String password = properties.getProperty("password");
        try {
            Class.forName(dirverClass);
            connection = DriverManager.getConnection(url, user, password);
            state = connection.prepareStatement(sql);
        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }

    private void close() {
        if (resultSet != null) {
            try {
                resultSet.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
        if (state != null) {
            try {
                state.close();
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

```