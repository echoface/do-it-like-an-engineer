# C++ 的委托构造函数

虽然一直在使用C++开发， 但是有个问题一直没有在意， 就是C++不同的编译器和版本不一定支持`委托构造函数（Delegating constructors）`， 如果说正式的支持委托构造函数， 是在C++11标准中正式确定的；我们先来看看在工作中遇到的一个问题， 其中一些细微的差别，导致的运行结果非常不一样：

## Case 1:

```c++
#include "stdio.h"

class CDelegate {
public:
    CDelegate() {
        printf("%s\n", "CDelegate() be called");
        CDelegate(0); //@ 这里我是在构造函数中调用的另外一个构造函数！！
    }
    CDelegate(int value) {
        printf("%s\n", "CDelegate(int value) be called");
        value_ = value;
    }
    ~CDelegate() {
        printf("%s\n", "CDelegate destroyed");
    };
    int get_vaule() {
        return value_;
    }
private:
    int value_;
};

int main(int argc, char const *argv[])
{
    /* code */
    CDelegate* delegate = new CDelegate();
    printf("value_: %d\n", delegate->get_vaule());
    //delete delegate;
    return 0;
}
```

* 上面的例子中,我是在无参数的构造函数的block中调用了 带参数的构造函数；
* 是通过无参数的构造函数创建的`CDelegate`对象
* 为了排除干扰，main函数中没有去调用`delete delegate`对象

## Case 1 输出

下面是运行结果：

```shell
CDelegate() be called
CDelegate(int value) be called
CDelegate destroyed
value_: 0
```

## Case 2

```c++
#include "stdio.h"

class CDelegate {
public:
    CDelegate(): CDelegate(0) { //这里是在初始化器中！！！！！
        printf("%s\n", "CDelegate() be called");
    }
    CDelegate(int value) {
        printf("%s\n", "CDelegate(int value) be called");
        value_ = value;
    }
    ~CDelegate() {
        printf("%s\n", "CDelegate destroyed");
    };
    int get_vaule() {
        return value_;
    }
private:
    int value_;
};

int main(int argc, char const *argv[])
{
    /* code */
    CDelegate* delegate = new CDelegate();
    printf("value_: %d\n", delegate->get_vaule());
    //delete delegate;
    return 0;
}
```

下面我们看看输出：如果我使用`g++ -std=gnu++11 main.cc` 或 `g++ -std=c++11 main.cc` 则不会出现警告⚠️；我使用的g++版本是ubuntu 16.04中自带的版本g++ 5.4

## Case 2 输出:

```shell
huan@Macmini:~/Desktop$ g++ main.cc
main.cc:5:26: warning: delegating constructors only available with -std=c++11 or -std=gnu++11
  CDelegate(): CDelegate(0) {
                          ^
huan@Macmini:~/Desktop$ ./a.out 
CDelegate(int value) be called
CDelegate() be called
value_: 0
```

为了更清楚的看看到底发生了什么， 我对case 1改造一下， 以便我们看清楚发生了什么：

## case 3

```c++
#include "stdio.h"

class CDelegate {
public:
    CDelegate() {
        printf("%s; this object is:%p\n", "CDelegate() be called", this);
        CDelegate(0);
    }
    CDelegate(int value) {
        printf("%s, this object is:%p\n", "CDelegate(int value) be called", this);
        value_ = value;
    }
    ~CDelegate() {
        printf("obj:%p going to die, %s\n", this, "CDelegate destroyed");
    };

    int get_vaule() {
        return value_;
    }
private:
    int value_;
};


int main(int argc, char const *argv[])
{
    /* code */
    CDelegate* delegate = new CDelegate();
    printf("using obj:%p get value_: %d\n", delegate, delegate->get_vaule());
    //delete delegate;
    return 0;
}
```

## Case 3 输出：

```shell
CDelegate() be called; this object is:0x13cfc20
CDelegate(int value) be called, this object is:0x7ffc4b06b4e0
obj:0x7ffc4b06b4e0 going to die, CDelegate destroyed
using obj:0x13cfc20 get value_: 0
```

## 分析与结论:

从case 1的输出可以看到， 如果我们在一个构造函数的函数体中去调用另一个构造函数， 实际上会发生另外一次构造函数和析构函数， 也就是说我们在构造函数CDelegate\(\) 中通过`CDelegate(int value)`构造了一个新的CDelegate对象，而这个对象作为一个临时变量，在构造函数`CDelegate()`运行完之后， 临时的对象就析构了；所以才会出现`CDelegate destroyed` 的打印输出； 在case 3中会印证这个想法；

case 2中是C++11文档中所写到的，c++11开始支持`委托构造函数` 但是， 委托构造函数必须放在`构造器列表当中`而不能放在函数体中，这是文档中明确要求的；从case2的运行输出中可以看到， 如果我们在构造函数的初始化器｛初始化列表｝中， 则不会出现case 1中会有一次析构的发生；

case 3中， 我将每一个类对象的指针都打印出来了， 从case 3的输出可以看出； case 1的情形下， 首先通过CDelegate\(\) 创建了具体的一个对象`0x13cfc20` ， 在这个函数体中， 我们又通过`CDelegate(int value)`创建了一个对象`0x7ffc4b06b4e0` 而这个对象在构造函数`CDelegate()`离开的时候作为临时变量被析构了；

而我在编程中就是犯了这个错误；最近在学apple 的swift中， 构造函数的委托都是放在具体的函数体中， 而我想当然的认为C++11以上的标准也会使用同样的策略（ps: 当然没有仔细想， 就想当然的用了）; 如此👀来， c++11等新的标准引入了大量的新的必要的特性， 包括我之前写的一个swift lambda表达式 和 c++中的一个对比， 包括值捕获，捕获列表；都非常的相似，但是同样的，swift作为后起之秀， 没有历史兼容等等包袱， 可以大刀阔斧的改进和使用优良的设计；包括switch case中默认的break，都能让程序跑起来更加的“意料之中”； 而不是意料之外；当然也不是没有缺点， 新的C++也足够足够的好，当程序语言，永远都没有最好；

所以，如果使用委托构造， 请一定要记得放在构造列表当中；

Reference:
---
https://msdn.microsoft.com/en-us/library/dn387583.aspx
https://thenewcpp.wordpress.com/2013/07/25/delegating-constructors/
http://stackoverflow.com/questions/13961037/delegate-constructor-c


