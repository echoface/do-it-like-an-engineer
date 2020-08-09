# 闭包中的捕获列表

官方文档中已经有说明“无论您将函数或闭包赋值给一个常量还是变量，您实际上都是将常量或变量的值设置为对应函数或闭包的引用”； 是个引用类型， 那么按照swift的ARC机制， 就会在产生在一个闭包中比较隐晦的捕获了外面的对象，通常都是类对象；比如`this`对象；

##### 注意:

> Swift 有如下要求：只要在闭包内使用`self`的成员，就要用`self.someProperty`或者`self.someMethod`\(而不只是`someProperty`或`someMethod`\)。这提醒你可能会不小心就捕获了`self`。

要在闭包中解决循环引用的问题，官方给出的方法就是在闭包中使用捕获列表，指明是`unowner`或者`weak`;从而来解决闭包内对外部的对象产生强引用关系；捕获列表中的每个元素都是由`weak`或者`unowned`关键字和实例的引用\(如`self`或`someInstance`\)成对组成。每一对都在方括号中，通过逗号分开。如果闭包没有参数；在捕获列表和`closure block`之间使用关键字`in` 分割开来；

```swift
@lazy var someClosure: () -> String = {
    [unowned self] in
    // closure body goes here
}
```

如果是存在闭包参数，那么就变成了下面这个样子了：

```swift
doSomeThingAsync(request: req, handle: {
  [unowner self, weak ohterInstance] (arg1, arg2...) in 

  //closure block, your code here
  ...
});
```

其中有几点在开发中依旧需要注意；

* 当闭包和捕获的实例总是互相引用时并且总是同时销毁时，将闭包内的捕获定义为`无主引用`。
* 当捕获引用有时可能会是`nil`时，将闭包内的捕获定义为`弱引用(weak)`。弱引用总是可选类型，并且当引用的实例被销毁后，弱引用的值会自动置为`nil`。这使我们可以在闭包内检查它们是否存在。
  > 如果捕获的引用绝对不会置为nil，应该用无主引用，而不是弱引用。

![](/MacIOS_development/img/closureReference2x.png)

swift中这种写法和思想其实和其它语言很想， 就像c++11 标准中的lambda表达式；它定义的闭包和swift中长得惊人的相似：

```c++
#include <algorithm>
#include <cmath>

void abssort(float* x, unsigned n) {
    std::sort(x, x + n,
        // Lambda expression begins
        [](float a, float b) {
            return (std::abs(a) < std::abs(b));
        } // end of lambda expression
    );
}
```

![](./img/IC251606.jpeg)

1. Capture 子句（在 C++ 规范中也称为 lambda 引导。）
2. 参数列表（可选）。 （也称为 lambda 声明符\)
3. 可变规范（可选）。
4. 异常规范（可选）。
5. 尾随返回类型（可选）。
6. “lambda 体”

Lambda 可在其主体中引入新的变量（用 C++14），它还可以访问（或“捕获”）周边范围内的变量。 Lambda 以 Capture 子句（标准语法中的 lambda 引导）开头，它指定要捕获的变量以及是通过值还是引用进行捕获。 有与号 \(&\) 前缀的变量通过引用访问，没有该前缀的变量通过值访问。空 capture 子句 \[ \] 指示 lambda 表达式的主体不访问封闭范围中的变量。

可以使用默认捕获模式（标准语法中的 capture-default）来指示如何捕获 lambda 中引用的任何外部变量：\[&\] 表示通过引用捕获引用的所有变量，而 \[=\] 表示通过值捕获它们。 可以使用默认捕获模式，然后为特定变量显式指定相反的模式。 例如，如果 lambda 体通过引用访问外部变量 total 并通过值访问外部变量 factor，则以下 capture 子句等效：

```c++
// 下面所有的写法都表示 对变量`factor`使用值捕获， 对`total`使用应用捕获
[&total, factor]
[factor, &total]
[&, factor]
[factor, &]
[=, &total]
[&total, =]
```

同时在`范形`中也可以使用变参

```
template<class... Args>
void f(Args... args) {
    auto x = [args...] { return g(args...); };
    x();
}
```



