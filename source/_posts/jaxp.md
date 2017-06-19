---
title: jaxp解析xml文档实现增删改查  

comments: true    

tags: jaxp

categories: 
    - DOM操作 
    - XML

description: jaxp解析xml文档

date: 2017-02-05 #文章生成時間
   
---


## 这是被解析的示例xml

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
            
**增加**

<!--more-->


        package cn.xml;
        
        import java.io.FileOutputStream;
        import java.io.OutputStream;
        
        import javax.xml.crypto.dsig.Transform;
        import javax.xml.parsers.DocumentBuilder;
        import javax.xml.parsers.DocumentBuilderFactory;
        import javax.xml.transform.*;
        import javax.xml.transform.dom.DOMSource;
        import javax.xml.transform.stream.StreamResult;
        
        import org.w3c.dom.Document;
        import org.w3c.dom.Element;
        import org.w3c.dom.Node;
        
        public class Demo03_xml_add {
            //4.向XML文档中添加节点 <售价>12元</售价>
            public void add() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                //在内存中的xml中创造一个节点
                Element price = document.createElement("售价");//得到标签
                price.setTextContent("12元");//添加标签中内容
        
                //先得到书节点 转换为标签
                Element book = (Element)document.getElementsByTagName("书").item(0);
                //把创造的节点添加到xml文档中书标签下
                book.appendChild(price);
                //此时只更新了内存中的XML文档(document对象指向的) 所以要把document对象指向的内存中的xml文档更新到硬盘中的xml文档
        
                //更新后的写入XML文档
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
            }
        
            //5.向XML文档中指定位置添加节点 <售价>999元</售价>
            public void add2() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                Element price = document.createElement("售价");
                price.setTextContent("999元");
        
                //得到参考节点 即下一个标签(Element是Node的一个子集 Element是Node的扩展)
                Element refNode = (Element) document.getElementsByTagName("售价").item(1);
        
                //得到要插入的节点
                Element book = (Element) document.getElementsByTagName("书").item(0);    
                //插入book节点的指定位置 把price节点插入refNode节点之前
                book.insertBefore(price, refNode);//参数也可以是标签  
        
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer tr = tf.newTransformer();
                tr.transform(new DOMSource(document), new StreamResult(new FileOutputStream("src/cn/xml/book.xml")));
            }
        
            //6.向XML文档中添加属性
            public void add3() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                //得到节点
                Element bookname = (Element) document.getElementsByTagName("书名").item(0);
                bookname.setAttribute("name", "XXX");
        
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer tr = tf.newTransformer();
                tr.transform(new DOMSource(document), new StreamResult(new FileOutputStream("src/cn/xml/book.xml")));
            }
        }
        

**删除**


        package cn.xml;
        
        import java.io.FileOutputStream;
        
        import javax.xml.parsers.DocumentBuilder;
        import javax.xml.parsers.DocumentBuilderFactory;
        import javax.xml.transform.Transformer;
        import javax.xml.transform.TransformerFactory;
        import javax.xml.transform.dom.DOMSource;
        import javax.xml.transform.stream.StreamResult;
        
        import org.w3c.dom.Document;
        import org.w3c.dom.Element;
        
        public class Demo03_xml_delete {
            public void delete() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                //得到要删除的节点
                Element price = (Element) document.getElementsByTagName("售价").item(2);
                //得到要删除节点的父节点
                Element book = (Element) document.getElementsByTagName("书").item(1);
                //通过父节点删除子节点
                book.removeChild(price);
        
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer tr = tf.newTransformer();
                tr.transform(new DOMSource(document), new StreamResult(new FileOutputStream("src/cn/xml/book.xml")));
            }
        
            public void delete2() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                Element price = (Element) document.getElementsByTagName("售价").item(3);
                //通过子节点得到父节点再删除自己
                price.getParentNode().removeChild(price);
                //其他:通过子节点得到父节点的父节点的父节点 (删除父节点)...删除整个xml文档中的节点
                //price.getParentNode().getParentNode().getParentNode().removeChild(price.getParentNode().getParentNode());
                //删除指定节点的属性
                //price.removeAttribute("color");
        
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer tr = tf.newTransformer();
                tr.transform(new DOMSource(document), new StreamResult(new FileOutputStream("src/cn/xml/book.xml")));
            }
        }


**更新**

        package cn.xml;
        
        import java.io.FileOutputStream;
        import java.io.IOException;
        
        import javax.xml.parsers.DocumentBuilder;
        import javax.xml.parsers.DocumentBuilderFactory;
        import javax.xml.transform.Transformer;
        import javax.xml.transform.TransformerFactory;
        import javax.xml.transform.dom.DOMSource;
        import javax.xml.transform.stream.StreamResult;
        
        import org.w3c.dom.Document;
        import org.w3c.dom.Element;
        import org.xml.sax.SAXException;
        
        public class Demo03_xml_update {
            public void update() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                Element price = (Element) document.getElementsByTagName("售价").item(1);
                price.setTextContent("123.456元");//更新标签中内容
                price.setAttribute("color", "eeed");//更新标签属性
        
                TransformerFactory tf = TransformerFactory.newInstance();
                Transformer tr = tf.newTransformer();
                tr.transform(new DOMSource(document), new StreamResult(new FileOutputStream("src/cn/xml/book.xml")));
            }
        }

**遍历**

        package cn.xml;
        
        import javax.xml.parsers.DocumentBuilder;
        import javax.xml.parsers.DocumentBuilderFactory;
        
        import org.w3c.dom.Document;
        import org.w3c.dom.Element;
        import org.w3c.dom.Node;
        import org.w3c.dom.NodeList;
        
        public class Demo03_xml_read{
                        //使用DOM方式对XML文档进行crud(增删改查)
        
            public void read1()  throws Exception{
        
            //1.创建工厂(得到DOM解析器的工厂实例)   ---这个工厂类是抽象类,so用其newInstance方法得到DOM的新实例
            DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
            //2.从DOM工厂获得DOM解析器 有了这个实例才可以解析
            DocumentBuilder builder =  factory.newDocumentBuilder();
            //3.将给定URI的内容解析为一个XML文档，并且返回一个新的DOM Document对象
            Document document = builder.parse("src/cn/xml/book.xml");
            //4.以后的处理都是对Document对象进行的
        
            //1.读取XML文档中<书名>....</书名>节点中的值
            NodeList list = document.getElementsByTagName("书名");//按文档顺序返回包含在文档中且具有给定标记名称的所有 Element 的 NodeList。 返回节点集合
            Node node = list.item(1);//取第二个"书名"的节点
            String s = node.getTextContent();//得到节点的文本内容
            System.out.println(s);
            }
        
            //2.遍历整个XML文档中的所有节点(标签)
            public void read2()  throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
                    //得到根节点
                Node root = document.getElementsByTagName("书架").item(0);//得到"书架"节点(根)
                    //得到孩子并打印
                this.glist(root);
                }
        
            private void glist(Node node){
                //instanceof 在运行时指出对象是否是特定类的一个实例 返回布尔值
                if(node instanceof Element){//判断node是不是标签(元素) (因为xml的空格和换行符也能传进来)
                    System.out.println(node.getNodeName());//打印节点名称
                    NodeList list = node.getChildNodes();//得到孩子节点 返回孩子节点的集合
                    for (int i = 0; i < list.getLength(); i++) {
                        Node child = list.item(i);
                        glist(child);
                    }
                }
            }
        
            //3.得到"书名"标签中属性值
            public void read3() throws Exception{
                DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
                DocumentBuilder builder =  factory.newDocumentBuilder();
                Document document = builder.parse("src/cn/xml/book.xml");
        
                NodeList list = document.getElementsByTagName("书名");
                //两种方法 第二个不推荐
                //把得到的"书名"节点强行转为标签类型
                Element bookname = (Element)list.item(0);
                String s = bookname.getAttribute("color");//此方法可取得属性值
        /*    
                Node bookname = list.item(0);
                String s= bookname.getAttributes().getNamedItem("color").getNodeValue();
        */
        
                System.out.println(s);
            }
        }