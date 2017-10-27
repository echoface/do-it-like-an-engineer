# C++ Static Assertion 静态断言

static assert用于在`编译时`的断言检测，也就是说，在编译器编译代码的时候，就检测这个条件是否成立， 如果检测失败`false` 则终止编译， 表示这里有某项必须满足的条件是不满足的

语法
---

>   **static_assert** **(** bool_constexpr **,** message **)** | (since C++11)
>   **static_assert** **(** bool_constexpr  **)**              | (since C++17)
                                                                  
其中 bool_constexpr 布尔表达式， 如果为`true` 则这个语句没有任何作用， 否则， 则在编译输出中输出 `message` 信息，并且终止编译；从c++17 开始`message`参数可以被忽略；

Note
---
因为`message` 必须是一个字符串字面量（`literal`）, 所以它不能包含动态的信息，也不能包含常量表达式等任何不是字面量的信息;


例子
---
```c++
static_assert(sizeof(void *) == 4, "64-bit code generation is not supported.");

```

如果上面的例子在64bit的机器上编译， 在编译的过程中就会报错；这也是`static assert`中static的意思；