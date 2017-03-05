---
title: 重新学习JDBC之获取statement

comments: true    

tags: 
    - JDBC

categories: 
    - JDBC

description: 

date: 2017-02-06
   
---

# **Statement类 **
获取connection(见 http://www.ay2626.me/index.php/2017/02/06/cxxxjdbc/) 之后, 需要获得sql语句并发送然后执行sql语句,所以有了本章
>直接看代码

```
private Connection getConnection(String sql) {
		Properties properties = new Properties();
		try {
				//获取配置文件中的数据库信息
				properties.load(this.getClass().getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties"));
		} catch (IOException e) {
				e.printStackTrace();
		}

		String dirverClass = properties.getProperty("driver");
		String url = properties.getProperty("jdbc_url");
		String user = properties.getProperty("user");
		String password = properties.getProperty("password");
		
		Connection connection = null;
        Statement state = null;
        try {
            //加载数据库驱动 
            Class.forName(dirverClass);
            //获取数据库连接
            connection = DriverManager.getConnection(url, user, password);
						
			//获取Statment对象
            state = connection.createStatement();
			//执行sql语句
            state.execute(sql);

        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }

        if (state != null) {//关闭statment对象,释放资源
            try {
                state.close();
            } catch (SQLException e) {
                System.out.println(e);
            }
        }
        if (null != connection) {//关闭connction对象,释放资源
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
}
```


---

# **升级**
Statement对象创建之后,没执行一次都会重新编译一次sql语句(sql语句是执行时候参数嘛),这很不好
所以我们用其子类PreparedStatement

1.  创建时的区别： 
	2.  Statement statement = conn.createStatement();
	3.  PreparedStatement preStatement = conn.prepareStatement(sql); 
4.  执行的时候: 
	5.   ResultSet rSet = statement.executeQuery(sql);
	6.    ResultSet pSet = preStatement.executeQuery();
看出，PreparedStatement有预编译的过程,已经绑定sql,之后无论执行多少遍,都不会再去进行编译,效率高

```
   private static Connection connection = null;
    private static PreparedStatement prep = null;

    private void getConnection(String sql) {
        Properties properties = new Properties();
        try {
            //获取配置文件中的数据库信息
            properties.load(this.getClass().getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties"));
        } catch (IOException e) {
            e.printStackTrace();
        }

        String dirverClass = properties.getProperty("driver");
        String url = properties.getProperty("jdbc_url");
        String user = properties.getProperty("user");
        String password = properties.getProperty("password");

        try {
            //加载数据库驱动
            Class.forName(dirverClass);
            //获取数据库连接
            connection = DriverManager.getConnection(url, user, password);
            prep = connection.prepareStatement(sql);
            prep.execute();//这里是更新操作的事例 如果是查询等其他则调用方法有不同

        } catch (SQLException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }


//执行数据库操作之后必须关闭各个对象(按顺序)
    public void close(Statement state, Connection connection) {
        if (state != null) {
            try {
                state.close();
            } catch (SQLException e) {
                System.out.println(e);
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
```
