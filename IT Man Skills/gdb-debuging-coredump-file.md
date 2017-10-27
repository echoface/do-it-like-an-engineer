# Gdb Debuging Coredump file

## 查看coredump文件中的backtrack

在gdb中， 有solib-absolute-prefix 和 solib-search-path两个参数可以用来指定

http://visualgdb.com/gdbreference/commands/set_solib-search-path

set solib-search-path /n	fs/gonghuan/mstar6486/out/Release/lib
:

- **set solib-search-path path1:path2**
> If this variable is set, path is a colon-separated list of directories to search for shared libraries. ‘solib-search-path’ is used after ‘sysroot’ fails to locate the library, or if the path to the library is relative instead of absolute. If you want to use ‘solib-search-path’ instead of ‘sysroot’, be sure to set ‘sysroot’ to a nonexistent directory to prevent gdb from finding your host's libraries. ‘sysroot’ is preferred; setting it to a nonexistent directory may interfere with automatic loading of shared library symbols.
```

- **show solib-search-path**
> Display the current shared library search path.


### 根据coredump 的log来与判断coredump的原因和位置
