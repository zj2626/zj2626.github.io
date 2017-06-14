---
title: dbcp, c3p0, druid工具类

comments: true    

tags: 
    - DBCP
    - C3P0
    - DRUID
    - 工具类

categories: 
    - JDBC

description: 

date: 2017-02-14
   
---

<h1>DBCP工具类</h1>

<pre><code>public class DBCPUtils {
    private static DataSource dataSource = null;

    static {
        Properties properties = new Properties();
        try {
            properties.load(DBCPUtils.class.getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties"));
            dataSource = BasicDataSourceFactory.createDataSource(properties);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public DBCPUtils() {
    }

    public static Connection getConnetcion(){
        Connection connection = null;
        try {
            connection = dataSource.getConnection();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return connection;
    }

    public static void releaseConnecion(Connection connection){
        if(null != connection){
            try {
                connection.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
</code></pre>

<!--more-->

```
#驱动
driverClassName=com.mysql.jdbc.Driver
#数据库连接地址
url=jdbc:mysql://127.0.0.1:3306/test?zeroDateTimeBehavior=convertToNull&useUnicode=true&characterEncoding=UTF-8
#用户名
username=root
#密码
password=anyao112233
#初始化连接
initialSize=10
#连接池的最大数据库连接数。设为0表示无限制
maxTotal=50
##最小空闲连接
minIdle=10
#最大空闲数，数据库连接的最大空闲数。超过空闲时间，数据库连接将被标记为不可用，然后被释放。设为0表示无限制
#空闲连接:意思就是连接了数据库而最大的没有向数据库发送请求的连接
maxIdle=50
#超过时间限制，回收没有用(废弃)的连接（默认为 300秒） 以秒为单位
removeAbandonedTimeout=60
#超过removeAbandonedTimeout时间后，是否进行没用连接（废弃）的回收（默认为false，调整为true)
removeAbandoned=true
#最大建立连接等待时间 超过此时间将异常 设为-1表示无限制 以毫秒为单位
maxWaitMillis=60000
#在空闲连接回收器线程运行期间休眠的时间值,以毫秒为单位. 如果设置为非正数,则不运行空闲连接回收器线程(每60秒运行一次空闲连接回收器)
timeBetweenEvictionRunsMillis=60000
#连接在池中保持空闲而不被空闲连接回收器线程(如果有)回收的最小时间值，单位毫秒(池中的连接空闲30s后被回收,默认值就是30分钟)
minEvictableIdleTimeMillis=300000

```

<h1>C3P0工具类</h1>

<pre><code>public class C3P0Utils {
    private static DataSource dataSource = null;

    private static ThreadLocal<Connection> threadLocal = new ThreadLocal<Connection>();

    static {
        //自动加载src下c3p0的配置文件【c3p0-config.xml】
        dataSource = new ComboPooledDataSource("myApp");
    }

    public C3P0Utils() {
    }
		
	public static void beginTransaction(Connection connection) {
			try {
					connection.setAutoCommit(false);
			} catch (SQLException e) {
					e.printStackTrace();
			}
	}

	public static void commitTransaction(Connection connection) {
			try {
					connection.commit();
			} catch (SQLException e) {
					e.printStackTrace();
			}
	}

    public static Connection getConnetcion() {
        Connection connection = threadLocal.get();//得到当前线程上绑定的连接
        try {
            if (connection == null || !connection.isClosed()) {
                //当前没有绑定连接
                connection = dataSource.getConnection();//新建连接
                threadLocal.set(connection);//将局部变量connection的值设置为conn
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return connection;
    }

    public static void releaseConnecion() {
        Connection connection = threadLocal.get();
        try {
            if (null != connection && !connection.isClosed()) {
                connection.close();
                //从线程局部变量中移除conn，如果没有移除掉，下次还会用这个已经关闭的连接，就会出错
                threadLocal.remove();
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }

    }
}
</code></pre>

```
<c3p0-config>
    <default-config>
        <property name="user">root</property>
        <property name="password">anyao112233</property>
        <property name="driverClass">com.mysql.jdbc.Driver</property>
        <property name="jdbcUrl">jdbc:mysql://localhost:3306/test</property>
        <property name="initialPoolSize">10</property>
        <property name="maxIdleTime">30</property>
        <property name="maxPoolSize">100</property>
        <property name="minPoolSize">10</property>
    </default-config>

    <named-config name="myApp">
        <property name="user">root</property>
        <property name="password">anyao112233</property>
        <property name="driverClass">com.mysql.jdbc.Driver</property>
        <property name="jdbcUrl">jdbc:mysql://localhost:3306/test</property>
        <property name="initialPoolSize">10</property>
        <property name="maxIdleTime">30</property>
        <property name="maxPoolSize">100</property>
        <property name="minPoolSize">10</property>
    </named-config>
</c3p0-config>
```

<h1>DRUID工具类</h1>

<code></code>
