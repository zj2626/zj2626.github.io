---
title: JDBC把文件作为数据对数据库的操作简单示例(Blob类型)

comments: true    

tags: 
    - Blob

categories: 
    - JDBC

description: 

date: 2017-02-10
   
---

# :如果是插入某个文件可以用mysql的Blob类型

#### *Blob类型,二进制大对象,用来存储二进制文件(图片等)*
下面是简单的示例

<!--more-->

```java
package com.jdbc;

import org.junit.Test;

import java.io.*;
import java.sql.*;
import java.util.Properties;

/**
 * Created by zj on 2017/2/10.
 */
public class insertBlob {
    @Test
    public void test() {
        InputStream inputStream = null;
        /*
		插入BLOB类型数据 (必须使用PreparedStatement)
        */
		try {
            inputStream = new FileInputStream("E:/app/Project/Test_Demo/src/java.jpg");
            insert("insert into teacher(name, birth, picture) values (?, ?, ?)",
                    "fucc", new Date(System.currentTimeMillis()), inputStream);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } finally {
            if (inputStream != null) {
                try {
                    inputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        /*
        查询并展示Blob类型数据
         */
        query("SELECT id id, name name, birth birth, picture picture FROM teacher WHERE id = ?",
                442);
    }

	//插入方法(其实删除,修改也可以使用)
	//插入Blob类型(mysql)需要传入InputStream类型
    public int insert(String sql, Object... args) {
        Connection connection = null;
        PreparedStatement state = null;
        int result = 0;

        try {
            connection = getConnection();
            state = connection.prepareStatement(sql);
            for (int i = 0; i < args.length; i++) {
                //专门用来设置blob类型的方法是state.setBlob(InputStream inputstream);
                state.setObject(i + 1, args[i]); //遍历设置占位符的值
            }
            result = state.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            close(connection, state, null);
        }

        return result;
    }

	//读取 读取Blob类型时, 需要用InputStream类型接收在用OutputStream读取到文件中方可访问
    public void query(String sql, Object... args) {
        Connection connection = null;
        PreparedStatement state = null;
        ResultSet resultSet = null;
        InputStream inputStream = null;
        OutputStream outputStream = null;

        try {
            connection = getConnection();
            state = connection.prepareStatement(sql);
            for (int i = 0; i < args.length; i++) {
                //专门用来设置blob类型的方法是state.setBlob(InputStream inputstream);
                state.setObject(i + 1, args[i]); //遍历设置占位符的值
            }
            resultSet = state.executeQuery();
            while (resultSet.next()) {
                int id = resultSet.getInt(1);
                String name = resultSet.getString(2);
                Date date = resultSet.getDate(3);
                Blob picture = resultSet.getBlob(4);
                System.out.println(id + " " + name + " " + date + " " + picture);

				//读取文件(Blob->InputStream->OutputStream->文件)
				inputStream = picture.getBinaryStream();
                outputStream = new FileOutputStream("pic.jpg");
                byte[] bytes = new byte[50];
                int len;
                while ((len = inputStream.read(bytes)) != -1) {
                    outputStream.write(bytes, 0, len);
                }
            }
        } catch (SQLException | IOException e) {
            e.printStackTrace();
        } finally {
            if(outputStream != null){
                try {
                    outputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            if(inputStream != null){
                try {
                    inputStream.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            close(connection, state, resultSet);
        }
    }

    private Connection getConnection() {
        Connection connection = null;
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
        } catch (SQLException | IOException | ReflectiveOperationException e) {
            e.printStackTrace();
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