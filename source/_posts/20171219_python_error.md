---
title: TypeError, a bytes-like object is required, not 'str'

comments: true

tags: 
    - python
    - 转码

categories: 
    - BUG解决

description: str和bytes类型之间的常用转码方式

toc: true

---

> 问题分析: 该问题主要是由于当前操作的字符串是bytes类型的字符串对象，并对该bytes类型的字符串对象进行按照str类型的操作。

{% qnimg 20171226111345.png title:问题 alt:问题 extend:?imageView2/2/w/600 %}

* 解决办法，将s转码成为str类型

{% qnimg 20171226111804.png title:问题 alt:问题 extend:?imageView2/2/w/600 %}

<!--more-->

## str和bytes类型之间的常用转码方式

> str to bytes

```python
s = 'ab bbb'
print (type(s))

b = bytes(s, encoding = 'utf-8')
print (type(b))

b2 = s.encode('utf-8')
print (type(b2))

b3 = str.encode(s)
print (type(b3))
```

{% qnimg 20171226115104.png title:问题 alt:问题 extend:?imageView2/2/w/600 %}

> bytes to str

```python
b = b'abbbb'
print (type(b))

s = str(b, encoding = 'utf-8')
print (type(s))


s2 = b.decode()
print (type(s2))

s3 = b.decode('utf-8')
print (type(s3))


s4 = bytes.decode(b)
print (type(s4))
```

{% qnimg 20171226115528.png title:问题 alt:问题 extend:?imageView2/2/w/600 %}



> 转载自 链接地址: http://blog.csdn.net/bible_reader/article/details/53047550

> 个人博客 欢迎来访： http://zj2626.com