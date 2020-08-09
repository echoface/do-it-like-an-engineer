# Linux Dynamic Library anylize

参考IBM文档库的说明： 只能说IBM的文档库是对所有人的良心之作呀， 相比之下， google的文档库更像是英语世界的天堂;

reference:

* [dynamic-libraries](http://www.ibm.com/developerworks/cn/linux/l-dynamic-libraries/)
* [static-link vs dynamic link](http://stackoverflow.com/questions/1993390/static-linking-vs-dynamic-linking)

non-PIC 与 PIC 代码的区别主要在于 access global data, jump label 的不同。比如一条 access global data 的指令;

* non-PIC 的形势是：
  ```
  ld r3, var1  
  ```

* PIC 的形式则是：
  ```
  ld r3, var1-offset@GOT
  ```

  > 意思是从 GOT 表的 index 为 var1-offset 的地方处
  > 指示的地址处装载一个值,即var1-offset@GOT处的4个 byte 其实就是 var1 的地址。这个地址只有在运行的时候才知道，是由 dynamic-loader\(ld-linux.so\) 填进去的。


再比如 jump label 指令

* non-PIC 的形势是：
  ```
  jump printf ，意思是调用 printf。
  ```

* PIC 的形式则是：
  ```
  jump printf-offset@GOT,
  ```

  > 意思是跳到 GOT 表的 index 为 printf-offset 的地方处指示的地址去执行，
  > 这个地址处的代码摆放在 .plt section，


每个外部函数对应一段这样的代码，其功能是通过dynamic-loader\(ld-linux.so\) 来查找函数的地址\(本例中是 printf\)，然后将其地址写到 GOT 表的 index 为 printf-offset 的地方，
同时执行这个函数。这样，第2次呼叫 printf 的时候，就会直接跳到 printf 的地址，而不必再查找了。

GOT 是 data section, 是一个 table, 除专用的几个 entry，每个 entry 的内容可以再执行的时候修改；
PLT 是 text section, 是一段一段的 code，执行中不需要修改。
每个 target 实现 PIC 的机制不同，但大同小异。比如 MIPS 没有 .plt, 而是叫 .stub，功能和 .plt 一样。

可见，动态链接执行很复杂，比静态链接执行时间长;但是，极大的节省了 size，PIC 和动态链接技术是计算机发展史上非常重要的一个里程碑。

