---
title: jaxp解析XML

comments: true    

tags: jaxp

categories: 
    - DOM操作 
    - XML

description:  jaxp解析xml文档

date: 2017-02-05 #文章生成時間
   
---

```java
package cn.utils;
//包名

import java.io.FileOutputStream;

import javax.xml.crypto.dsig.Transform;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.w3c.dom.Document;

//工具类 执行那些重复的代码块 默认为静态
public class XmlUtils {
    private static String filename = "src/exam.xml";

    //得到解析器并解析xml文档
    public static Document getDocument() throws Exception{
        //1.创建工厂(得到DOM解析器的工厂实例)   ---这个工厂类是抽象类,so用其newInstance方法得到DOM的新实例
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        //2.从DOM工厂获得DOM解析器 有了这个实例才可以解析
        DocumentBuilder builder =  factory.newDocumentBuilder();
        //3.将给定URI的内容解析为一个XML文档，并且返回一个新的DOM Document对象
        Document document = builder.parse("src/cn/xml/book.xml");
        //4.以后的处理都是对Document对象进行的

        return document;
    }

    //把得到的数据写入xml文档
    public static void write2Xml(Document document) throws Exception{
        TransformerFactory factory = TransformerFactory.newInstance();//产生转化器
        Transformer tf = factory.newTransformer();
        tf.transform(new DOMSource(document), new StreamResult(new  FileOutputStream(filename)));

        //原理
        /*
                //创建工厂实例
                TransformerFactory tf = TransformerFactory.newInstance();
                //通过工厂实例得到Transformer对象(transform方法可以转化来源到目的地)
                Transformer tr = tf.newTransformer();
                //DOMSource是Source的实现类 把Document类型封装为Source类型
                Source s = new DOMSource(document);
                //声明输出流对象 指向硬盘中的XML文件
                OutputStream f= new FileOutputStream("src/cn/xml/book.xml");
                //把输出流对象通过流方法转化为Result对象 Result对象指向硬盘中的XML文件
                Result r = new StreamResult(f);
                //transform方法(来源, 目的地) 把s写入r
                tr.transform(s, r);


        */
    }
}
```
