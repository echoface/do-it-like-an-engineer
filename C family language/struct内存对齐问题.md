# Struct内存对齐问题



面试题爱考，实际上没什么意义

这个问题可以说是很多职场上问的很多的问题，有的公司也将它作为必考题，虽说实际大部分人编程可能不需要care这些事情；就像大部分C++ programmer并不需要关心也不使用C++的元编程一样...;

这个问题引用网络上的一句总结吧：

**背书式**：各成员变量存放的起始地址相对于结构的起始地址的偏移量必须为该变量的类型所占用的字节数的倍数 各成员变量在存放的时候根据在结构中出现的顺序依次申请空间 同时按照上面的对齐方式调整位置 空缺的字节自动填充 同时为了确保结构的大小为结构的字节边界数(即该结构中占用最大的空间的类型的字节数)的倍数，所以在为最后一个成员变量申请空间后 还会根据需要自动填充空缺的字节;

网络上有各种各样的解释. 《深入理解计算机系统》中有比较明确的对齐的定义与解释, 对齐是为了CPU指令流水线更加高效的取指,寻址. 上面的话其实对应着下面几个原则.

- 每一个成员变量存放的起始地址为变量大小的整数倍.
- 结构体起始地址为其成员结构最大成员的整数倍.
  - 很对人疑惑为什么需要这一条规则, 其实思考一下连续对象数组就能很容易理解了, eg: A a_list[2];  第二个成员同样需要满足第一条原则. 如果起始地址不对齐, 那么第二个成员中最大成员就没法满足第一条规则.

编译器的实现会限制这个条款的正确性， 包括变量、函数对齐等等编译参数，都可以改变这个对齐；

**不可以同时用const和static修饰成员函数。** 但是普通的变量可以是static const哦， 一个是作用域和生命周期，一个是限定内容的只读性

