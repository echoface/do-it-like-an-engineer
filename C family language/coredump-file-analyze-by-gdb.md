##gdb coredump 文件的分析方法##

我们分析一个coredump， 前提条件是我们有对应产生coredump的文件， 还要有可执行文件和它所依赖的那部分库文件， 库不全没关系， 只要产生coredump的那部分有即可， 但是需要这些库的符号`symbol`没有被我们strip掉， 可以不需要编译的时候的`-g`参数；

命令：`gdb [excutable_file] [coredumpfile]`

在gdb中， 我们可以通过gdb命令`solib-absolute-prefix` 和 `solib-search-path`两个参数可以用来指定我们程序依赖的库的路径，以便gdb将这些库导入与coredump中的堆栈地址整合进行分析. 若有多个路径用冒号`:`分隔；

[gdb reference guide book](http://visualgdb.com/gdbreference/commands/set_solib-search-path)

example:
---
> set solib-search-path /nfs/gonghuan/mstar6486/out/Release/lib:/opt/mslib


- **set solib-search-path path**

> If this variable is set, path is a colon-separated list of directories to search for shared libraries. ‘solib-search-path’ is used after ‘sysroot’ fails to locate the library, or if the path to the library is relative instead of absolute. If you want to use ‘solib-search-path’ instead of ‘sysroot’, be sure to set ‘sysroot’ to a nonexistent directory to prevent gdb from finding your host's libraries. ‘sysroot’ is preferred; setting it to a nonexistent directory may interfere with automatic loading of shared library symbols.
```

- **show solib-search-path**

> Display the current shared library search path.