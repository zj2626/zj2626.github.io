---
title: sax解析xml文档(用javabean封装xml文档)

comments: true    

tags: sax

categories: 
    - DOM操作 
    - XML

description:  sax解析xml文档

date: 2017-02-05 #文章生成時間
   
---

**被解析的xml示例**

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
            <售价>12元</售价></书>
    </书架>
```

<!--more-->

**封装用的javabean**

```
    package cn.sax;
    //这是封装用的类
    public class BookObject {
        private String name;
        private String author;
        private String price;
    
        public String getName() {
            return name;
        }
        public void setName(String name) {
            this.name = name;
        }
        public String getAuthor() {
            return author;
        }
        public void setAuthor(String author) {
            this.author = author;
        }
        public String getPrice() {
            return price;
        }
        public void setPrice(String price) {
            this.price = price;
        }
    }
    ```
    **解析**
    ```
    package cn.sax;
    
    import java.awt.print.Book;
    import java.io.IOException;
    import java.util.ArrayList;
    import java.util.List;
    
    import javax.xml.parsers.ParserConfigurationException;
    import javax.xml.parsers.SAXParser;
    import javax.xml.parsers.SAXParserFactory;
    
    import org.junit.Test;
    import org.xml.sax.Attributes;
    import org.xml.sax.SAXException;
    import org.xml.sax.XMLReader;
    import org.xml.sax.helpers.DefaultHandler;
    
    public class sax解析xml_javabean封装xml {
    
        @Test
        public void main() throws ParserConfigurationException, SAXException, IOException {
            //1.创建解析工厂 抽象工厂
            SAXParserFactory factory = SAXParserFactory.newInstance();
            //2.得到解析器
            SAXParser parser = factory.newSAXParser();
            //3.得到读取器
            XMLReader reader = parser.getXMLReader();
            //4.设置内容处理器 读取使xml内容放在list中的book对象中
            BeanListHandler hand = new BeanListHandler();
            reader.setContentHandler(hand);
            //5.读取文档内容 解析xml文档
            reader.parse("src/book.xml");
            List list = hand.getBooks();
            System.out.println(list);
        }
    }
    
    //把xml文档中的每一本书封装到每个book对象中 并把多个book对象放在List集合中返回
    class BeanListHandler extends DefaultHandler{
        private List list = new ArrayList();
        private String currentTag;//解析到的当前的标签名称(所有)
        private BookObject book;//book对象封装得到的book标签
    
        @Override
        public void startElement(String uri, String localName, String qName,
                Attributes attributes) throws SAXException {//开始标签
            currentTag = qName;
            if("书".equals(currentTag)){
                //如果是书 就要用一个book对象来封装这个书
                book = new BookObject();
            }
        }
    
        @Override
        public void characters(char[] ch, int start, int length)
                throws SAXException {                   //内容
            if("书名".equals(currentTag)){//如果标签是 书名 则创造字符串对象放标签的内容
                String name = new String(ch, start, length);
                book.setName(name);
            }
            if("作者".equals(currentTag)){
                String author = new String(ch, start, length);
                book.setAuthor(author);
            }
            if("售价".equals(currentTag)){
                String price = new String(ch, start, length);
                book.setPrice(price);
            }
        }
    
        @Override
        public void endElement(String uri, String localName, String qName)
                throws SAXException {                   //结束标签
            currentTag = null;//currentTag不能不清空 以为解析xml文档会读取到空格和换行 干扰 空指针异常
            if ("书".equals(qName)) {
                list.add(book);//把book对象加入到list中
                book = null;//book对象置空
            }
        }
    
        //由于list对象是私有的 所以需要这个 
        public List getBooks() {
            return list;
        }
    }
```