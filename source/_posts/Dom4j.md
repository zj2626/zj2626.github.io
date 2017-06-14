---
title: Dom4j解析xml文档实现增删改查

comments: true    

tags: Dom4j

categories: 
    - DOM操作 
    - XML

description:  Dom4j解析xml文档

date: 2017-02-05 #文章生成時間
   
---


**这是被解析的xml文档示例**
```
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
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
                <售价>12元</售价>
            </书>
        </书架>
```
-------------------------------------------------------------------------


<!--more-->

```
    package cn.xml;
    
    import java.io.File;
    import java.io.FileNotFoundException;
    import java.io.FileOutputStream;
    import java.io.FileWriter;
    import java.io.IOException;
    import java.io.OutputStreamWriter;
    import java.io.UnsupportedEncodingException;
    import java.util.Iterator;
    import java.util.List;
    
    import org.dom4j.Document;
    import org.dom4j.DocumentException;
    import org.dom4j.DocumentHelper;
    import org.dom4j.Element;
    import org.dom4j.io.OutputFormat;
    import org.dom4j.io.SAXReader;
    import org.dom4j.io.XMLWriter;
    import org.junit.Test;
    
    public class Dom4j {
        @Test
        public void read() throws DocumentException{//读
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            Element root = document.getRootElement();//得到根节点 "书架"
            Element book = (Element) root.elements("书").get(1);//得到"书"节点中第二个"书"节点
            String value = book.element("书名").getText();//得到售"书名"节点的内容
            String attribute = book.element("书名").attribute("color").getValue();//得到属性值
            String attribute1 = book.element("书名").attributeValue("color");//得到的同上
    
            System.out.println(value);
            System.out.println(attribute);
            System.out.println(attribute1);
        }
    
        //@Test
        public void add() throws DocumentException, IOException{//增
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            Element book = document.getRootElement().element("书");//得到第一本书
            book.addElement("售价").setText("45元");//在书上添加售价节点 同时添加节点内容
    
            OutputFormat format = new OutputFormat().createPrettyPrint();//格式化输出器
            format.setEncoding("UTF-8");//设置格式化输出器的编码为UTF-8编码 使document按照utf-8格式输出
    
            //把修改写入文件 document是UTF-8编码的
            //XMLWriter writer = new XMLWriter(new FileWriter("src/book.xml"));//可能出现乱码
            //OutputStreamWriter可以指点采用什么字符集编码
            XMLWriter writer = new XMLWriter(new FileOutputStream("src/book.xml"), format);
            writer.write(document);//把document对象写入
            writer.close();//关闭流
        }
    
        //@Test
        public void add2() throws DocumentException, IOException{//在指定位置添加(通过更改保存所有孩子的List集合顺序)
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            Element book = document.getRootElement().element("书");//得到第一本书
            List list = book.elements();//得到所有的孩子 [书名, 孩子, 售价]
    
            //创建要加入的标签 以及内容
            Element helper = DocumentHelper.createElement("其他");
            helper.setText("内容");
    
            //加入list集合 需要把加入位置的元素移动到下一位 然后把其加入到位置(自动)
            list.add(2, helper);//添加到第三个位置
    
            OutputFormat format = new OutputFormat().createPrettyPrint();//格式化输出器
            format.setEncoding("UTF-8");
    
            XMLWriter writer = new XMLWriter(new FileOutputStream("src/book.xml"), format);
            writer.write(document);//把document对象写入
            writer.close();//关闭流
        }
    
        //@Test
        public void delete() throws DocumentException, IOException{//删除
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            Element price = document.getRootElement().element("书").element("售价");//得到售价节点
            price.getParent().remove(price);//用父母删孩子
    
            OutputFormat format = new OutputFormat().createPrettyPrint();//格式化输出器
            format.setEncoding("UTF-8");
    
            XMLWriter writer = new XMLWriter(new FileOutputStream("src/book.xml"), format);
            writer.write(document);//把document对象写入
            writer.close();//关闭流
        }
    
        @Test
        public void update() throws Exception{//更新
            SAXReader reader = new SAXReader();//解析器
            Document document = reader.read(new File("src/book.xml"));//解析
    
            Element book = (Element)document.getRootElement().elements("书").get(1);
            book.element("书名").setText("初日");
    
    
            OutputFormat format = new OutputFormat().createPrettyPrint();//格式化输出器
            format.setEncoding("UTF-8");
    
            XMLWriter writer = new XMLWriter(new FileOutputStream("src/book.xml"), format);
            writer.write(document);//把document对象写入
            writer.close();//关闭流
        }
    }
```
