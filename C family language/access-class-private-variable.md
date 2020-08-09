# c++ access class private variable

> 看下面这段代码：

```cpp
#include <iostream>
using namespace std;
class test{
      private:
            int a;
            int b;
      public:
            test(int a = 1, int b = 2){
                  this->a = a;
                  this->b = b;
            }
            int re(test ccc){
                  a = ccc.a + 444;// pos 1
                  b = ccc.b + 444;// pos 2
            }
};
```

为什么能访问私有变量？
---

咋样一看， 额为什么re函数中；我们能直接通过test类的对象ccc访问ccc这个对象的私有成员a， b呢；不是说private是私有和受保护的吗？


其实这和c++的实现有关, 因为同一个类的对象是类的友元类;不知道的复习下**`友元类`**.
