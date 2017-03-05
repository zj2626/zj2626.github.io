---
title: Vue学习笔记

comments: true    

tags: 
    - Vue

categories: 
    - 框架相关
    - 前端技术

description:

date: 2017-03-1
   
---

## Vue.js 是一套构建用户界面的 渐进式框架 JavaScript MVVM库 它是以数据驱动和组件化的思想构建的,无需手动操作DOM.

# MVVM模式

## Model-View-ViewModel

ViewModel是Vue.js的核心，它是一个Vue实例。Vue实例是作用于某一个HTML元素上的，这个元素可以是HTML的body元素，也可以是指定了id的某个元素。

当创建了ViewModel后，双向绑定是如何达成的呢？

首先，我们将DOM Listeners和Data Bindings看作两个工具，它们是实现双向绑定的关键。
从View侧看，ViewModel中的DOM Listeners工具会帮我们监测页面上DOM元素的变化，如果有变化，则更改Model中的数据；
从Model侧看，当我们更新Model中的数据时，Data Bindings工具会帮我们更新页面中的DOM元素。
<摘自: http://www.cnblogs.com/rik28/p/6024425.html>