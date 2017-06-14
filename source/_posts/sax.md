---
title: sax解析xml文档实现打印xml(遍历全部和指定位置)

comments: true    

tags: sax

categories: 
    - DOM操作 
    - XML

description:  sax解析xml文档

date: 2017-02-05 #文章生成時間
   
---

**这是示例被解析xml**
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


**遍历全部**
```
        package cn.sax;
        
        import java.io.IOException;
        
        import javax.sql.rowset.spi.XmlReader;
        import javax.xml.parsers.ParserConfigurationException;
        import javax.xml.parsers.SAXParser;
        import javax.xml.parsers.SAXParserFactory;
        
        import org.junit.Test;
        import org.xml.sax.Attributes;
        import org.xml.sax.ContentHandler;
        import org.xml.sax.Locator;
        import org.xml.sax.SAXException;
        import org.xml.sax.XMLReader;
        
        public class sax解析xml {
            @Test
            public void main() throws ParserConfigurationException, SAXException, IOException {
                //1.创建解析工厂 抽象工厂
                SAXParserFactory factory = SAXParserFactory.newInstance();
                //2.得到解析器
                SAXParser parser = factory.newSAXParser();
                //3.得到读取器
                XMLReader reader = parser.getXMLReader();
                //4.设置内容处理器
                reader.setContentHandler(new ListHandler());
                //5.读取文档内容 解析xml文档 解析一点就调用处理器处理 所以要先设置内容处理器
                reader.parse("src/book.xml");
            }
        
        }
        
        //内容处理器 得到xml文档所有内容
        class ListHandler implements ContentHandler{
                            //实现接口中的方法
            @Override
            public void startElement(String uri, String localName, String qName,
                    Attributes atts) throws SAXException {//当得到开始标签时 调用这个方法
                // TODO Auto-generated method stub
                System.out.print("<" + qName );//打印
        
                //获取属性 还要判断属性有没有(是否为null)
                for (int i = 0; atts != null && i < atts.getLength(); i++) {
                    String att_Name = atts.getQName(i);
                    String att_Vlaue = atts.getValue(i);
                    System.out.print(att_Name + "=" + att_Vlaue);
                }
        
                System.out.println( ">");
            }
        
            @Override
            public void characters(char[] ch, int start, int length)
                    throws SAXException {                       //当解析到标签中内容时就调用这个方法
                // TODO Auto-generated method stub
                System.out.println(new String(ch, start, length));//String解码(要解码的字符集,要解码的第一个byte位置,解码的长度)
            }
        
            @Override
            public void endElement(String uri, String localName, String qName)
                    throws SAXException {                       //当解析到结束标签时 调用这个方法
                // TODO Auto-generated method stub
                System.out.println("</"+ qName +">");
            }
        
        
            @Override
            public void setDocumentLocator(Locator locator) {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void startDocument() throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void endDocument() throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void startPrefixMapping(String prefix, String uri)
                    throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void endPrefixMapping(String prefix) throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void ignorableWhitespace(char[] ch, int start, int length)
                    throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void processingInstruction(String target, String data)
                    throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
            @Override
            public void skippedEntity(String name) throws SAXException {
                // TODO Auto-generated method stub
        
            }
        
        }
```
**遍历指定标签**
```
         //打印指定标签的值(这里指定第二个作者的值)
        package cn.sax;
        
        import java.io.IOException;
        
        import javax.xml.parsers.ParserConfigurationException;
        import javax.xml.parsers.SAXParser;
        import javax.xml.parsers.SAXParserFactory;
        
        import org.junit.Test;
        import org.xml.sax.Attributes;
        import org.xml.sax.SAXException;
        import org.xml.sax.XMLReader;
        import org.xml.sax.helpers.DefaultHandler;
        
        
        public class sax解析获得指定标签的值{
            @Test
            public void main() throws ParserConfigurationException, SAXException, IOException {
                //1.创建解析工厂 抽象工厂
                SAXParserFactory factory = SAXParserFactory.newInstance();
                //2.得到解析器
                SAXParser parser = factory.newSAXParser();
                //3.得到读取器
                XMLReader reader = parser.getXMLReader();
                //4.设置内容处理器
                reader.setContentHandler(new TagValueHandler());
                //5.读取文档内容 解析xml文档
                reader.parse("src/book.xml");
            }
        }
        
        //获取指定标签的值
        class TagValueHandler extends DefaultHandler{
            private String currentTag;//用来记住当前解析到的是什么标签
            private int needNumber = 2;     //需要的标签是第几个标签
            private int currentNumber; //当前解析到的是第几个标签
        
            @Override
            public void startElement(String uri, String localName, String qName,
                    Attributes attributes) throws SAXException {
                // TODO Auto-generated method stub
                super.startElement(uri, localName, qName, attributes);//可以不写
        
                currentTag = qName;
                if(currentTag.equals("作者")){
                    currentNumber++;
                }
            }
        
            @Override
            public void endElement(String uri, String localName, String qName)
                    throws SAXException {
                // TODO Auto-generated method stub
                super.endElement(uri, localName, qName);
        
                currentTag = null;//置空
            }
        
            @Override
            public void characters(char[] ch, int start, int length)
                    throws SAXException {
                // TODO Auto-generated method stub
                super.characters(ch, start, length);
        
                if("作者".equals(currentTag) && currentNumber==needNumber){ 
                    System.out.println(new String(ch, start, length));
                }
            }
        
        }

```