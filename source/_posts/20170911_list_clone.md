---
title: 待完成

comments: true    

tags: 
    - C语言

categories: 
    - 数据结构和算法

description: 

---
http://www.cnblogs.com/lyajs/p/5779021.html
        
<!--more-->        

        package collection;
        
        import org.junit.Test;
        
        import java.util.ArrayList;
        import java.util.ArrayList;
        
        /**
         * Created by zj on 2017/9/11.
         */
        public class Link {
        
            @Test
            public void test() {
                ArrayList<Student> list = new ArrayList<>();
                //添加两个元素
                Student stJack = new Student("Jack", "AAAA");
                Student stTom = new Student("Tom", "BBBBB");
                list.add(stJack);
                list.add(stTom);
                //克隆
                ArrayList<Student> listCopy = new ArrayList<>();
                /*list.forEach(li -> {
                    listCopy.add(li);
                });*/
                listCopy = (ArrayList<Student>) list.clone();
        
                listCopy.get(1).setId("FFFFFFFFFFF");
                System.out.println(list);
                System.out.println(list.get(1).hashCode());
                System.out.println(listCopy);
                System.out.println(listCopy.get(1).hashCode());
        
                /*ArrayList<String> ArrayList = new ArrayList<>();
                ArrayList.add("A");
                ArrayList.add("B");
                ArrayList.add("C");
                ArrayList.add("D");
                ArrayList.add("E");
        
                System.out.println(ArrayList.clone());
        
                ArrayList.forEach(li -> {
                    System.out.println(li);
                });*/
            }
        }
        
        
        package collection;
        
        import java.util.HashSet;
        import java.util.Set;
        
        /**
         * Created by zj on 2017/9/10.
         */
        public class Student {
            private String id;
            private String name;
            private Set courses;
        
            public Student() {
            }
        
            public Student(String id, String name) {
                this.id = id;
                this.name = name;
                this.courses = new HashSet();
            }
        
            public Student(String id, String name, Set courses) {
                this.id = id;
                this.name = name;
                this.courses = courses;
            }
        
            @Override
            public String toString() {
                return "Student{" +
                        "id='" + id + '\'' +
                        ", name='" + name + '\'' +
                        ", courses=" + courses +
                        '}';
            }
        
            @Override
            protected Object clone() throws CloneNotSupportedException {
                return new Student(this.id, this.name);
            }
        
            public String getId() {
                return id;
            }
        
            public void setId(String id) {
                this.id = id;
            }
        
            public String getName() {
                return name;
            }
        
            public void setName(String name) {
                this.name = name;
            }
        
            public Set getCourses() {
                return courses;
            }
        
            public void setCourses(Set courses) {
                this.courses = courses;
            }
        }


        public static void main(String[] args) {
                Map<String, Student> map = new HashMap<String, Student>();
        
                map.put("a", new Student("A", "FFF"));
                map.put("b", new Student("B", "AAA"));
                map.put("d", new Student("D", "KKK"));
                map.put("c", new Student("C", "KKK"));
        
                List<Map.Entry<String, Student>> list =
                        new ArrayList<>(map.entrySet());
        
                Collections.sort(list, new Comparator<Map.Entry<String, Student>>() {
                    @Override
                    public int compare(Map.Entry<String, Student> o1, Map.Entry<String, Student> o2) {
                        return o1.getValue().compareTo(o2.getValue());
                    }
                });
        
                for (Map.Entry<String, Student> mapping : list) {
                    System.out.println(mapping.getKey() + ":" + mapping.getValue());
                }
            }



> 个人博客 欢迎来访： http://zj2626.github.io