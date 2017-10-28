# javascript 构造函数

* 如果一个函数被定义为用于创建对象的**构造函数**， 使用时一定要用new， 
  > 在strict模式下，this.name = name将报错，因为this绑定为undefined，在非strict模式下，this.name = name不报错，因为this绑定为window，于是无意间创建了全局变量name，并且返回undefined，这个结果更糟糕。
  > 
  > * 为了区分普通函数和构造函数，按照约定，构造函数首字母应当**大写**，而普通函数首字母应当小写，这样，一些语法检查工具如jslint将可以帮你检测到漏写的new。


一个例子，对比C++中得类 &lt;===&gt; javascript中得构造函数
**MyObject中的this指的不是函数本身**

```js
//构造函数

 //使自己的对象多次复制，同时实例根据设置的访问等级可以访问其内部的属性和方法
 //当对象被实例化后，构造函数会立即执行它所包含的任何代码
 function MyObject(msg){
     //特权属性(公有属性) ====> C++类中得public 属性
     this.myMsg = msg; //只在被实例化后的实例中可调用
     this.address = '上海';

     //私有属性 =====> C++类中得private属性， 只能构造函数（类）中使用；
     var name = '豪情';
     var age = 29;
     var that = this;

     //私有方法 ====> private函数， 只能内部访问？
     function sayName(){
         alert(that.name);
     }
     //特权方法(公有方法)
     //能被外部公开访问
     //这个方法每次实例化都要重新构造而prototype是原型共享，所有实例化后，都共同引用同一个
     this.sayAge = function(){
         alert(name); //在公有方法中可以访问私有成员
     }
     //私有和特权成员在函数的内部，在构造函数创建的每个实例中都会包含同样的私有和特权成员的副本，
     //因而实例越多占用的内存越多, 通过公有方法，也就是把方法放到prototype中去
 }
 //公有方法 适用于通过new关键字实例化的该对象的每个实例

 //向prototype中添加成员将会把新方法添加到构造函数的底层中去
 myObject.prototype.sayHello = function(){
     alert('hello everyone!');
 }
 //静态属性 ====> C++类中得static 变量
 //适用于对象的特殊实例，就是作为Function对象实例的构造函数本身
 myObject.name = 'china';
 //静态方法 ====> C++类中得static 函数
 myObject.alertname = function(){
     alert(this.name);
 }

 //实例化
 var m1 = new MyObject('111');
 // m1.xxx 这样的方式能访问的只能是公开属性和函数，不能调用到m1.sayName是不能被访问的；而原型（基类）中添加的sayHello方法在对象实例化后能访问的m.sayhello();是ok的；

 //---- 测试属性 ----//
 //console.log(myObject.name); //china
 //console.log(m1.name); //undefined, 静态属性不适用于一般实例
 //console.log(m1.constructor.name); //china, 想访问类的静态属性，先访问该实例的构造函数，然后在访问该类静态属性
 //console.log(myObject.address); //undefined, myObject中的this指的不是函数本身，而是调用address的对象，而且只能是对象
 //console.log(m1.address); //上海 此时this指的是实例化后的m1

 //---- 测试方法 ----//
 //myObject.alertname(); //china,直接调用函数的类方法
 //m1.alertname(); //FF: m1.alertname is not a function, alertname 是myObject类的方法，和实例对象没有直接关系， 这和C++中得不一样额
 //m1.constructor.alertname(); //china, 调用该对象构造函数（类函数）的方法（函数）
 //m1.sayHello(); //hello everyone, myObject类的prototype原型下的方法将会被实例继承
 //myObject.sayHello(); //myObject.sayHello is not a function，sayHello是原型方法，不是类的方法

 //---- 测试prototype ----//
 //console.log(m1.prototype); //undefined, 实例对象没有prototype
 //console.log(myObject.prototype); //Object 
 //alert(myObject.prototype.constructor); //console.log返回myObject(msg)，此时alert()更清楚，相当于myObject
 //console.log(myObject.prototype.constructor.name); //china, 相当于myObject.name;
```

![](Javascript nodejs/img/javascript_prototype01.jpg)
![](Javascript nodejs/img/javascript_prototype02.png)

---



##### 参考：

[http:\/\/www.cnblogs.com\/mrsunny\/archive\/2011\/05\/09\/2041185.html](http://www.cnblogs.com/mrsunny/archive/2011/05/09/2041185.html)
[http:\/\/www.cnblogs.com\/RicCC\/archive\/2008\/02\/15\/JavaScript-Object-Model-Execution-Model.html](http://www.cnblogs.com/RicCC/archive/2008/02/15/JavaScript-Object-Model-Execution-Model.html)

##### 发现有人对上图做了解释，分享：

[http:\/\/www.cnblogs.com\/daishuguang\/p\/3978409.html](http://www.cnblogs.com/daishuguang/p/3978409.html)
[http:\/\/www.cnblogs.com\/wangfupeng1988\/p\/3979985.html](http://www.cnblogs.com/wangfupeng1988/p/3979985.html)
[http:\/\/anykoro.sinaapp.com\/2012\/01\/31\/javascript%E4%B8%ADfunctionobjectprototypes\_\_proto\_\_%E7%AD%89%E6%A6%82%E5%BF%B5%E8%AF%A6%E8%A7%A3\/](http://anykoro.sinaapp.com/2012/01/31/javascript%E4%B8%ADfunctionobjectprototypes__proto__%E7%AD%89%E6%A6%82%E5%BF%B5%E8%AF%A6%E8%A7%A3/)

