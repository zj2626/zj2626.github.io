---
title: Jdbc实现简单的事务处理

comments: true    

tags: 
    - 事务

categories: 
    - JDBC

description: 

date: 2017-02-10
   
---

<!--more-->

```
package com.jdbc;

import org.junit.Test;

import java.io.IOException;
import java.sql.*;
import java.util.Properties;

/**
 * Created by zj on 2017/2/10.
 */
public class ACID {
    /*
        JDBC实现数据库事务操作
        1.原子性(事务不可分割)
        2.一致性(一致性状态-->另一个一致性状态)
        3.隔离性(类似于加锁, 某一刻一个数据只能被一个事务操作)
        4.持久性(事务提交,数据库的改变就是永久的)

        要实现 需要多个操作使用同一个连接(Connection)
     */
    @Test
    public void test() {
        Connection connection = null;
        try {
            connection = getConnection("update student set f_age = f_age + " + 2 + " where f_id = " + 1, null);
            connection = getConnection("update student set f_age = f_age * " + 10 + " where f_id = " + 1, connection);
            connection.commit();//如果前面的操作都成功,手动提交事务
        } catch (SQLException e) {
            if (connection != null) {
                try {
                    connection.rollback();//有异常就回滚事务
                } catch (SQLException e1) {
                    e1.printStackTrace();
                }
            }
        } finally {
            close(connection, null, null);//关闭
        }
    }

    private Connection getConnection(String sql, Connection connection) throws SQLException {
        int result;
        PreparedStatement preparedStatement = null;
        try {
            Properties properties = new Properties();
            properties.load(this.getClass().getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties"));
            String dirverClass = properties.getProperty("driver");
            String url = properties.getProperty("jdbc_url");
            String user = properties.getProperty("user");
            String password = properties.getProperty("password");

            Class.forName(dirverClass);
            if (connection == null) {
                connection = DriverManager.getConnection(url, user, password);
                //取消自动提交(Connection的默认提交行为)
                connection.setAutoCommit(false);
            }
            preparedStatement = connection.prepareStatement(sql);
            result = preparedStatement.executeUpdate();
            System.out.println(result);
        } catch (IOException e) {
            throw new RuntimeException();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } finally {
            close(null, preparedStatement, null);
        }

        return connection;
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

```