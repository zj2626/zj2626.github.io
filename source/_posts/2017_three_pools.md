---
title: dbcp,c3p0,druid简单实例(包含配置介绍)

comments: true    

tags: 
    - DBCP
    - C3P0
    - DRUID

categories: 
    - 数据库连接池

description: 

date: 2017-02-13
   
---

# **三种连接池的配置:dbcp、c3p0、druid**

<!--more-->

# dbcp
 ## 1.硬编码方式
 
           @Test
            public void testDBCPCode() {
                //BasicDataSource实现接口DataSource   DBCP连接池核心类
                BasicDataSource dataSouce = new BasicDataSource();
                dataSouce.setDriverClassName("com.mysql.jdbc.Driver");  //驱动
                dataSouce.setUrl("jdbc:mysql://127.0.0.1:3306/test");   //数据库连接字符串
                dataSouce.setUsername("root");                          //数据库用户名
                dataSouce.setPassword("anyao112233");                   //数据库密码
                dataSouce.setInitialSize(5);                            //设置初始化连接数
                dataSouce.setMaxTotal(5);                               //设置最大连接数
                dataSouce.setMaxWaitMillis(10000);                      //设置申请连接最大等待时间
                dataSouce.setRemoveAbandonedTimeout(60);                //设置空闲连接时长 超过就回收没用的连接
                Connection connection = null;
                try {
                    connection = dataSouce.getConnection();
        //            connection.prepareStatement("update student set f_name = 'fuk' where f_id = 10").executeUpdate();
                    System.out.println(connection.getClass() + "\n" + connection.getMetaData() + "\n");
                } catch (SQLException e) {
                    e.printStackTrace();
                } finally {
                    // 关闭
                    if (connection != null) {
                        try {
                            connection.close();
                        } catch (SQLException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
            

 ## 2.配置方式
 *文件jdbc.properties*
 
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
        


           @Test
            public void testDBCPXML() throws Exception {
                Connection connection = null;
                try {
                    Properties prop = new Properties();
                    InputStream inStream = this.getClass().getClassLoader()
                                .getResourceAsStream("jdbc.properties");
                    prop.load(inStream);
                    System.out.println(prop);
                    // 根据prop配置，直接创建数据源对象(BasicDataSourceFactory工厂)
                    DataSource dataSouce = BasicDataSourceFactory.createDataSource(prop);
                    // 获取连接
                    connection = dataSouce.getConnection();
        //            connection.prepareStatement("delete from student where f_id=1").executeUpdate();
                } catch (SQLException e) {
                    e.printStackTrace();
                } finally {
                    // 关闭
                    if (connection != null) {
                        try {
                            connection.close();
                        } catch (SQLException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }
 
 
 ---
 
 # ** C3P0**
 
 ## 1.硬编码方式
 
       @Test
        public void testC3P0Code() throws Exception {
            // 创建连接池核心工具类
            ComboPooledDataSource dataSource = new ComboPooledDataSource();
    
            dataSource.setJdbcUrl("jdbc:mysql://localhost:3306/test");
            dataSource.setDriverClass("com.mysql.jdbc.Driver");
            dataSource.setUser("root");
            dataSource.setPassword("anyao112233");
            dataSource.setInitialPoolSize(3);//连接池初始化时创建的连接数
            dataSource.setMaxPoolSize(6);//连接池中拥有的最大连接数
            dataSource.setMaxIdleTime(1000);
            Connection connection = null;
            try {
                connection = dataSource.getConnection();
                connection.prepareStatement("delete from student where f_name like '%name%'").executeUpdate();
            } catch (SQLException e) {
                e.printStackTrace();
            } finally {
                if (connection != null) {
                    try {
                        connection.close();
                    } catch (SQLException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
 
 
  ## 2.配置方式
  
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
	
	
		@Test
		public void testC3P0XML() throws Exception {
				// 创建c3p0连接池核心工具类
				// 自动加载src下c3p0的配置文件【c3p0-config.xml】
				//如果要使用default-config无需传参数，
				//如果要使用named-config里面配置初始化数据源，则只要使用一个带参数的ComboPooledDataSource构造器就可以了
				DataSource dataSource = new ComboPooledDataSource("myApp");
				Connection connection = null;
				try {
						connection = dataSource.getConnection();
						connection.prepareStatement("delete from student where f_id = 20").executeUpdate();
				} catch (SQLException e) {
						e.printStackTrace();
				} finally {
						if (connection != null) {
								try {
										connection.close();
								} catch (SQLException e) {
										e.printStackTrace();
								}
						}
				}
			}

 ---
 
 # ** DRUID**
 
 ## 1.硬编码方式
 
 
  ## 2.配置方式
	
	