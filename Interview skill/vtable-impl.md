# cplusplus 虚表的实现

在C＋＋中， 动态绑定或者说late binding 是通过虚表来实现的， 书上着么说， 但是始终没能比较深刻的理解这一部分，后来辗转搜寻， 终于在quora上找到个像样的答案；



To implement virtual functions, C++ uses a special form of late binding known as the virtual table or vTable. The **virtual table** is a lookup table of functions used to resolve function calls in a dynamic/late binding manner.

Every class that uses virtual functions (or is derived from a class that uses virtual functions) is given its own virtual table.

This table is simply a static array that the compiler creates at compile time. A virtual table contains one entry for each virtual function that can be called by objects of the class.

Each entry in this vTable is simply a Function Pointer that points to the most-derived function accessible by that class ie the most Base Class.

The compiler also adds a hidden pointer to the base class, which we will call *__vPtr.

\*__vPtr is set (automatically) when a class instance is created so that it points to the virtual table for that class. *__vPtr is inherited by derived classes,

let’s take a look at a simple example

```
class Base
{
public:
  virtual void function1() {};
  virtual void function2() {};
};

class D1: public Base
{
public:
  virtual void function1() {};
};
class D2: public Base
{
public:
  virtual void function2() {};
};
```

Because there are 3 classes here, the compiler will set up 3 virtual tables: one for Base, one for D1, and one for D2.

The compiler also adds a hidden pointer to the most Base class that uses virtual functions.

```c
class Base
{
public:
  FunctionPointer \*__vptr;
  virtual void function1() {};
  virtual void function2() {};
};
class D1: public Base
{
public:
  virtual void function1() {};
};
class D2: public Base 
{
public:
  virtual void function2() {};
};
```

When a class object is created, *__vPtr is set to point to the virtual table for that class. For example, when a object of type Base is created, *__vPtr is set to point to the virtual table for Base. When objects of type D1 or D2 are constructed, *__vPtr is set to point to the virtual table for D1 or D2 respectively.

Because there are only two virtual functions here, each virtual table will have two entries (one for function1(), and one for function2()).

Base’s virtual table is simple. An object of type Base can only access the members of Base. Base has no access to D1 or D2 functions. Consequently, the entry for function1 points to Base::function1(), and the entry for function2 points to Base::function2().

D1’s virtual table is slightly more complex. An object of type D1 can access members of both D1 and Base. However, D1 has overridden function1(), making D1::function1() more derived than Base::function1(). Consequently, the entry for function1 points to D1::function1(). D1 hasn’t overridden function2(), so the entry for function2 will point to Base::function2().

D2’s virtual table is similar to D1, except the entry for function1 points to Base::function1(), and the entry for function2 points to D2::function2().

Here’s a picture of this graphically:

<canvas class="qtext_image_placeholder landscape qtext_image zoomable_in_feed" width="492" height="483" data-src="data:image/GIF;base64,R0lGODdhCgAKAIAAAAAAAP///ywAAAAACgAKAAAIQQADCBxIsKBAAAEABFjIMACAAAACAAhAsaLFixgtAggAIIDHjwEABAAQoKTJAAACAAjAsmUAAAEABJhJMwCAmwEBADs=" style="visibility: hidden;"></canvas>![](https://qph.ec.quoracdn.net/main-qimg-9bfc157fe7324e86a095fc58b03555e7?convert_to_webp=true)

By using these tables, the compiler and program are able to ensure function calls resolve to the appropriate virtual function, even if you’re only using a pointer or reference to a base class.