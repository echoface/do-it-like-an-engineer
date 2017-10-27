# C/C++ 中字符串字面量

今天编程时遇到了一个比较有意思的问题，关于C/C++变量在内存中的组织，研究了一下，分享如下：

首先，请看如下代码片段：

```c
 1 int main() {
 2     char *s_literal = "This is literal string.";
 3     char s_array[] = "This is literal string.";
 4     cout << "Modifying on s_array..."
 5     s_array[0] = 'A';
 6     cout << s_array << endl;
 7     cout << "Modifying on s_literal..."
 8     s_literal[0] = 'A';
 9     cout << s_literas_literal << endl;
10 }
```

程序的焦点主要在第二行和第三行，第二行声明的s_literal变量叫做**字符串字面量（string literal）**，而第三行所做的是将一个字符串字面量拷贝到了一个char型数组里。这两行程序看似相似，实则差别很大。

如下是以上程序的输出结果（平台：_osx10.10，LLVM 6.0 + clang-600.0.56_）：

```sh
Modifying on s_array...
Ahis is literal string.
Modifying on s_literal...
Bus error: 10
```

这里`Bus error 10`是由于CPU试图修改非法地址所引起的，也就是说我们对`s_literal`所指向内容的修改是非法的。

为什么我们不能对这个字符串数组进行修改呢？

原因很简单，因为它是只读的。你可能会纳闷，我们并没有在`s_literal`前面加`const`修饰符啊，它怎么变成只读的了呢？这个问题的原因在于`s_literal`所指向的是一个[<font color="red">字符串字面量(string literal)</font>](https://en.wikipedia.org/wiki/String_literal)。

在C/C++中,**字符串字面量是一个编译时便初始化好的静态变量**，该类型存储在只读空间。按照标准所述，对其的修改将引发未定义行为(undefined behavior)。在我的mac上显示的是`bus error`，也有系统报`segmentation error`的，都是修改了只读空间的原因。其实该变量是直接与code存储在一起的，在Windows环境下，我们可以通过用记事本(notepad)打开一个编译链接好的，定义有string literal的exe文件，通过搜索便可以看到定义的字符串。这么看只读属性就是理所应当了，exe文件的一部分当然是不允许修改的。

另外，**字符串字面量的生命周期是与该程序等长的**，即自从包含字符串字面量的代码被载入，直到程序退出，字符串字面量将一直存在于内存当中。当字符串字面量有了以上两点性质，它就有了一个可以优化的地方。我们姑且叫做[字符串字面量的池化(stirng literal pooling)](https://en.wikipedia.org/wiki/Literal_pool)，即C/C++编译器会维护一个字符串字面量池，使得内容相同的字符串字面量可以共享相同的内存空间，从而降低内存的不必要消耗。池化的实例请见下文。

现在，你可能又会问了，程序的第三行不也是把一个字符串字面量赋给了一个字符串数组么，为什么s_array变量就可以进行修改？答案是，`char s_array[]`声明了一个字符串数组，而`char *s_literal`仅仅声明了一个指针。所以第三行其实做了一个字符串的拷贝工作。具体来讲，第二行和第三行中所声明的字符串字面量因为其内容相同，所以编译器只会在字符串字面量池中开辟一份存储空间供第二行和第三行共享使用。第二行直接声明了一个指向这个空间的首地址的指针，而第三行将这个空间的内容复制到了一个根据其大小开辟的等长字符串数组里（该数组存储在栈空间中，下文会讲到），并将其命名为`s_array`变量。因此，`s_array`就是一个局部变量，对其修改与其他局部变量没有不同。

其实，像第二行这样的字面量声明方法已经不被C++标准提倡了，编译时会报warning。我们在平时编程时也应该避免这种用法。你也许会问，只有char类型存在字面量的概念么？其实并不是。大多数基本类型都有对应的字面量类型，比如`int a = 1;`中的"`1`"就是一个字面量，只不过编译器不允许我们用指针直接指向这些类型的字面量。所以他们也就不存在以上的这种错误。**但是我们应该了解当我们定义一个int型并且直接对其初始化时，实际上是将一个存在代码区的int字面量copy给了该变量**。

## 举一反三

由这个问题我们能够联想到其他一些相关的问题，即：

1.  既然对字符串字面量的写操作引起了地址非法错误，那么`string_literal`所指向的字符串的地址与普通字符串有什么区别？

2.  由C/C++对于string literal存储的管理引申出C/C++对其他变量的存储管理。

其实以上两个问题可以归结为一个问题，即

### C/C++是如何对变量的存储空间进行管理的？

首先我们需要了解C/C++都有哪些变量存储区域，根据变量的类型，C/C++中有如下**4个变量存储区域**(按照其各自地址从小到大排序)：

1.  代码区(code area)
2.  全局变量区(global variable area)
3.  堆区(heap area)
4.  栈区(stack area)

下面的程序输出展示了这四个区在程序中的实际地址：

```bash
--------Code Area--------
$                                string_literal = 0x100224e16
$                        another_string_literal = 0x100224e5f
$another_string_literal_with_same_value(pooled) = 0x100224e5f
                    --------Global Area--------
$                         const_static_variable = 0x100224f98
$                               static_variable = 0x10022502c
$                        global_static_variable = 0x100225030
$                               global_variable = 0x100225028
                    --------Heap Area--------
$                               malloc_variable = 0x7ff130403770
$                                  new_variable = 0x7ff130403780
                    --------Stack Area--------
$                                const_variable = 0x7fff5f9dbb2c
$                                local_variable = 0x7fff5f9dbb28
```

程序的源代码如下：

```c
#include <stdio.h>
#include <stdlib.h>

static int gv21 = 1;
int gv22 = 1;
int main() {
    int max_width = 46;
    char* v1 = "a";
    printf("                  --------Code Area--------\n");
    printf("$%*s = %p\n", max_width, "string_literal", v1);
    char *v11 = "b";
    printf("$%*s = %p\n", max_width, "another_string_literal", v11);
    char *v12 = "b";
    printf("$%*s = %p\n", max_width, "another_string_literal_with_same_value(pooled)", v12);
    printf("                  --------Global Area--------\n");
    const static int v31 = 1;
    printf("$%*s = %p\n", max_width, "const_static_variable", &v31);
    static int v2 = 1;
    printf("$%*s = %p\n", max_width, "static_variable", &v2);
    printf("$%*s = %p\n", max_width, "global_static_variable", &gv21);
    printf("$%*s = %p\n", max_width, "global_variable", &gv22);
    printf("                  --------Heap Area--------\n");
    int *v4 = (int *)malloc(sizeof(int));
    printf("$%*s = %p\n", max_width, "malloc_variable", v4);
    int *v5 = new int(1);
    printf("$%*s = %p\n", max_width, "new_variable", v5);
    printf("                  --------Heap Area--------\n");
    const int v3 = 1;
    printf("$%*s = %p\n", max_width, "const_variable", &v3);
    int v6 = 1;
    printf("$%*s = %p\n", max_width, "local_variable", &v6);
}
```

下面回答第一个问题：

从程序的输出可知，字符串字面量存储在所有变量地址空间中最小的部分，该部分是只读的。而普通的字符串变量存储在栈区或者堆区，这与int型其实并没有区别。

这个程序引出了一个[C/C++如何管理变量存储空间](/How_C_CPP_Manage_Variable_Storage.html)的问题，这个问题我会在[下一篇blog](/How_C_CPP_Manage_Variable_Storage.html)中略表拙见。在此我们仅对字面量相关进行探讨。

由上可见，**字符串字面量保存在地址最小的代码区**，而且它们会被池化(体现在`v11`和`v12`两个指针因内容相同指向了同一个地址)。

## 总结

**<font color="red">字符串字面量</font>**是C/C++在编译时便绑定在程序中的静态只读变量，存储在具有只读属性的代码区，对其的修改将引发未定义行为(undefined behavior)，一般表现为运行时错误。其实字面量并不限于字符串型，大多数基本类型都具有对应的字面量类型。大多数编译器版本都会维护一个**字面量池(literal pool)**来优化程序存储空间，字面量池使得具有相同内容的字面量共享一份存储空间。