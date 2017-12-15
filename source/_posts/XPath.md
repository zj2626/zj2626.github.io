---
title: XPath解析xml文档

comments: true    

tags: XPath

categories: 
    - DOM操作 
    - XML

description:  XPath解析xml文档

date: 2017-02-05 #文章生成時間
   
---

<!--more-->

**这是被解析的xml文档示例**
```xml
    <?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <用户>
        <user id="1"  username="aaa" password="123"  email="abc.com"/>
        <user id="2"  username="bbb"  password="123"  email="abc.com"/>
        <书架>
            <书>
                <书名>java实战</书名>
                <作者>张三</作者>
                <售价>121元</售价>
                <售价>12元</售价>
            </书>
            <书>
                <书名 color="yellow" name="XXX">c测试</书名>
                <作者>李四</作者>
                <售价 color="rrr">54元</售价>
                <售价>12元</售价></书>
        </书架>
    </用户>
```
------------------------------------------------------------------------------

```java
    package cn.xml;
    
    import java.io.File;
    
    import org.dom4j.Document;
    import org.dom4j.DocumentException;
    import org.dom4j.Node;
    import org.dom4j.io.SAXReader;
    import org.junit.Test;
    
    //用XPath提取xml文档数据
    public class Xpath{
        @Test
        public void read() throws DocumentException {
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            String s = document.selectSingleNode("//作者").getText();//得到第一个作者的内容
            //selectSingleNode是取第一个"作者"节点 要取所有则用selectNodes
            System.out.println(s);
        }
    
        @Test
        public void find() throws DocumentException {//检测xml文档中有没有相匹配的用户账号密码
            String username = "aaa";
            String password = "123";
    
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            //选择含有属性username且其值为'aa'的user元素( 这里注意空格有无是不同的)
            Node node = document.selectSingleNode("//user[@username= '" + username + "'  and @password= '" + password + "'  ]");
            if (node == null) {
                System.out.println("用户名/密码错误");
            }else{
                System.out.println("登陆成功");
            }
        }
    }
```