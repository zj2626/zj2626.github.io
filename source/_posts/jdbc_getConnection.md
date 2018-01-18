---
title: 重新学习JDBC之获取连接

comments: true    

tags: 
    - JDBC

categories: 
    - JDBC

description: 

date: 2017-02-06
   
---

**JDBC是一种用于执行sql语句的javaAPI, 为多种关系数据库提供统一访问有java编写的类和接口组成**

jdbc其实就是一种规范(基准),根据其可以自己构建更高级的框架,如(hibernate等),
编程人员须根据这个规范编写来操作数据库

----------------

<!--more-->

## >**Driver** 提供了一个接口 数据库厂商需要自己的产品编写此接口的实现类 通过创建实现类的对象(注册)加载相应的数据库驱动

## *1,原始的jdbc尝试(获取数据库连接)*

>*连接需要某个厂商的数据库驱动包 这里连接mysql  
官网下载地址  https://dev.mysql.com/downloads/connector/j/      里面的 mysql-connector-java-*.jar文件

    
         @Test
        public void testDriver() throws SQLException {
            //创建Driver实现类(这里是mysql的实现类) 同时注册驱动(见下面mysql源码参照1)
            Driver driver = new com.mysql.jdbc.Driver();
                    
            //Properties类用于读取java的配置文件(.properties) 这里并没有读取文件
            String url = "jdbc:mysql://127.0.0.1:3306/test"; //数据库地址
            Properties properties = new Properties();
            properties.put("user", "root"); //数据库用户名
            properties.put("password", "anyao112233");//数据库密码
                    
            //获取数据库连接 返回一个Connection的mysql的实现类
            Connection connection = driver.connect(url, properties);//见下面源码参照2
    
            System.out.println(connection);
        }

>*mysql的源码参照1*


            package com.mysql.jdbc;
            //一旦声明了此类的对象就会先调用这里静态代码块中的代码 实现驱动的注册(registerDriver)
            public class Driver extends NonRegisteringDriver implements java.sql.Driver {
                    public Driver() throws SQLException {
                    }
        
                    static {
                            try {
                                    //其实在注册的时候就已经实例化过一次driver对象 不需要自己new或newInstance
                                    //但是,由于此实例化为匿名,so只能自己再实例一遍,以获得实例化的对象
                                    DriverManager.registerDriver(new Driver());
                            } catch (SQLException var1) {
                                    throw new RuntimeException("Can\'t register driver!");
                            }
                    }
            }
	
	
> *mysql的源码参照2*

        
        package com.mysql.jdbc;
        public class NonRegisteringDriver implements Driver {
            public Connection connect(String url, Properties info) throws SQLException {
                            //检测url是否为空(现在URL是jdbc:mysql://127.0.0.1:3306/test)
                            if(url != null) {
                                    //检测url是否以后者开头---否
                                    if(StringUtils.startsWithIgnoreCase(url, "jdbc:mysql:loadbalance://")) {
                                            return this.connectLoadBalanced(url, info);
                                    }
                                    //检测url是否以后者开头---否
                                    if(StringUtils.startsWithIgnoreCase(url, "jdbc:mysql:replication://")) {
                                            return this.connectReplicationConnection(url, info);
                                    }
                            }
                            Properties props = null;
                            //获取url中信息存放到props对象中(HOST,user,password,DBNAME)
                            if((props = this.parseURL(url, info)) == null) {
                                    return null;
                            } else {
                                    try {
                                            //以props中的信息创建数据库连接 返回代表连接的对象
                                            com.mysql.jdbc.Connection ex = ConnectionImpl.getInstance(this.host(props), this.port(props), props, this.database(props), url);
                                            //返回连接对象
                                            return ex;
                                            //下面是各种异常
                                    } catch (SQLException var6) {
                                            throw var6;
                                    } catch (Exception var7) {
                                            SQLException sqlEx = SQLError.createSQLException(Messages.getString("NonRegisteringDriver.17") + var7.toString() + Messages.getString("NonRegisteringDriver.18"), "08001");
                                            sqlEx.initCause(var7);
                                            throw sqlEx;
                                    }
                            }
                    }
        }
        
        
*各位看官, 自己可以debug调试看看流程 其实也不难看懂,人家的代码都写得很清楚了*
----

## **2,升级版本**

配置文件内容
![](http://www.zj2626.com/wp-content/uploads/2017/02/aaa.png)(如图,地址要加字符编码,防止中文乱码)

            
        @Test
            public void test2() {
                getConnection();
            }
        
            //把获取数据库连接封装为一个类,把数据库的信息存放到配置文件中
            //原因:一般程序部署以后就不会再更改代码,如果数据有变,就可以只是更改配置文件,
            //    而要是这些信息放在代码中,则需要重新编译运行才能生效
            private Connection getConnection() {
                String dirverClass;
                String url;
                String user;
                String password;
        
                //读取文件
                //getClassLoader返回类的类加载器 
                //getResourceAsStream把指定目录的内容返回到一个输入流中
                InputStream inputStream = getClass().getClassLoader().getResourceAsStream("com/jdbc/jdbc.properties");
                Properties properties = new Properties();
                try {
                    //读取输入流中的内容到properties对象中
                    properties.load(inputStream);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                //按照键值对的形式读取对象中该键所对应的值 获取到数据库信息
                dirverClass = properties.getProperty("driver");
                url = properties.getProperty("jdbc_url");
                user = properties.getProperty("user");
                password = properties.getProperty("password");
        
                Properties info = new Properties();
                info.put("user", user);
                info.put("password", password);
        
                Driver driver;
                Connection connection = null;
                try {
                    //forName用于使JVM加载指定的类(全类名,写在配置文件中),即动态加载和创建Class 对象
                    //所有类都是Class类的对象
                    //通过刚才加载的Class对象(也就是你需要的)来实例化加载了的所需类的对象,效果同new一个对象
                    driver = (Driver) Class.forName(dirverClass).newInstance();
                    //获取连接
                    connection = driver.connect(url, info);
                    System.out.println(connection);
                } catch (InstantiationException | IllegalAccessException | ClassNotFoundException | SQLException e) {
                    e.printStackTrace();
                } finally {
                    if (connection != null) {
                        try {
                            connection.close();//关闭连接
                        } catch (SQLException e) {
                            e.printStackTrace();
                        }
                    }
                }
        
                return null;
            }
            
---

## **3,再次升级版本**

此时发现,通过Driver类直接控制数据库连接太麻烦,于是有了DriverManager
>DriverManager用来管理数据库中所有的驱动程序,把driver的创建,获取连接等过程交由DriverManager管理

        
        @Test
            public void test() {
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
                Connection connection = null;
                try {
                    //加载数据库驱动 可以多个驱动程序注册(在注册时候就已经实例化了一个对象,不需要自己新建driver对象)
                    Class.forName(dirverClass);
                    //获取数据库连接
                    //获取的时候会扫描所有的注册的驱动 找到合适的驱动然后获取连接
                    connection = DriverManager.getConnection(url, user, password);
                    System.out.println(connection);
                } catch (SQLException | ClassNotFoundException e) {
                    e.printStackTrace();
                }
            }
