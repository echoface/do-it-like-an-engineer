# 构造函数、析构函数与赋值运算符

条款05： 了解C++默认编写并调用哪些函数
---

一个空类，编译器会为它加上**默认构造函数（default构造函数）、析构函数、拷贝构造、拷贝赋值**四个public inline的实现；

注意⚠️： 编译器产生的析构函数时none-virtual的；这在某些情况下是非常危险的，比如说子类析构函数无法得到调用；

编译器会拒绝为class内部拥有const成员的类生成copy assignment operator；其实很好理解const 成员必须要**优先完成binding**；所以下面这个代码：

```c++
class B {
public:
    B(int& a): a_(a) {
    }
private:
    int& a_;
};

int main() {
    int i1 = 7;
    int i2 = 5;
    B b(i1);
    B b2(i2);

//copy_assignment.c:3:7: error: cannot define the implicit copy assignment operator for 'B',
//because non-static reference member 'a_' cannot use copy assignment operator
    //b = b2; //这里若取消注释， 你会得到一个编译错误
   
    return 0;
}
```

这个问题在stackoverflow上同样有很多讨论，比如说：

- [c-operator-method-for-const-references](http://stackoverflow.com/questions/3408804/c-operator-method-for-const-references)
- [assignment-operator-with-reference-members](http://stackoverflow.com/questions/7906127/assignment-operator-with-reference-members)

总之， 对于这个，我们应该拒绝❌！用下一个条款06；


条款06: 如不想使用编译器自动生成的函数，应该明确拒绝
---

某些对象（类）我们不希望被拷贝或者不应该被拷贝、赋值；那么我们应该明确的拒绝，否则一不小心就被编译器悄悄的生成了一份；解决办法就是拒绝编译器为我们生成；考虑两点，我们什么不做， 编译器会悄悄的生成一份，另一个就是我们自己声明一份，这样编译器就不会默认生成了【可我们是要阻止copying呀！】；

我们既要自己声明一份，又要不能被使用；这里要注意，编译器为我们生成的是public line的， 这也是我们解决这个问题的方法， 我们只要将它们**声明为private**的就可以了；注意⚠️！这里用的是声明， 我们不定义它！ 这样才能阻止friend， 和成员函数同样被禁止使用它们！

这个条款中同样提到一个良好的设计，就是声明一个不可拷贝的空基类，而任何其他我们不愿意发生cp，assignmeng的类继承它，因为调用之类的cp、copy assignment时， 会使用基类的成员，而基类我们已经明确拒绝了，那么这个机制就得到了很好的保证；

```c++
class Uncopyable {
protected:
	Uncopyable() {};
	~Uncopyable() {};
Private:
	Uncopyable(const Uncopyable&);
	Uncopyable& operator=(const Uncopyable&);
}
```


条款07: 为基类声明virtual析构函数
---

对于条款07， 每一个C++程序员应该把他作为基本的思维之一！

条款08: 别让异常逃离析构函数
---

在构造和析构函数中都应该要杜绝异常；虽然C++支持异常捕获机制，但是在构造函数和析构函数中，它们并不那么好用，甚至带来无法发现灾难； 我个人理解，如果真的有异常，发生的**初始化过程**，用单独的Init函数和DeInit函数并像库、函数、的使用者施加强制的说明和约束更加有效；



条款09： 绝不要再构造和析构函数中调用virtual函数；
---

在构造和析构的过程中，虚函数不会下降至derrived class对象的实现， 这和虚函数的实现有关系，C++的继承关系的调用过程：基类的构造函数->之类的构造函数-RUN->之类的析构函数->基类的析构；所以在基类的构造过程中， 之类还没能构建，所以调用的virtual函数运行的是本身的实现， 如果是纯虚函数，那么就是个错误；

条款九中指出的解决方案值得思考和借鉴，利用构造函数提供具体的信息给基类，以此来保证这种行为不会在构造和析构的时候发生；

条款10:令operator=返回一个*this的引用
---

这条和我以前看的C语言的技巧和设计范例中的规则性如初一则，保持链式表达式调用回让代码更好看并且好用！看下面的一个例子：

```c
void operation_f(type arg_in, type* arg_out);
type* operation_f(type arg_in);
operation_f(argin)->dothings();
```
也就是说，我们希望得到一个左值引用作为返回值；

```cpp
T& operator=(const T& rhs);
```
同样，对于+= -= *= =等等运算符都应该遵循这个准则；

条款11: 在operator=中处理自我赋值；
---

- 加入证同测试
- 通过拷贝构造+swap来实现
- 精妙的设计语句顺序

对于第二点，虽然书中的说法让人接受，但是实际上，编码的复杂度其实也在变高；不过对于这个问题， 我觉得有必要时刻保持警醒；有时候错误往往难以让人发现；


条款12: 复制对象时不要遗忘每一个成员
---

对于编译器自动生成的**复制**，编译器可以保证每一个对象都被复制到，但是，它并不能保证是我们想要的结果，比如说heap内存的部分；而对于我们自己实现的版本，编译器却不会帮我们检查遗漏的项；所以我们得小心翼翼地处理；我遇到的更多的情况是，多个人维护一个类；当新人往类中添加新的成员或者内容是， 他往往不一定知道你**从载了赋值操作和拷贝构造**；这个是个让人头疼的问题；还有文中提到的这种情况：

```cpp
class D: public B {
public:
	D& operator=(const D& d) {
		//B::operator=(d);  标记1
		p = d.p;
		return *this;
	}
private:
	int p;
};
```

标记1处的代码才是最容易忘记的，即使这个类和对象由你维护，稍不注意就犯下了错误、而且很难在事后再检查出来；

**所以记住**⚠️：
- 记得复制所有local长远变量
- 调用所有基类适当的copying函数

