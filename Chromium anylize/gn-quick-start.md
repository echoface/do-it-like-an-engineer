# GN 快速使用手册

## Contents

* [Running GN](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Running-GN)
* [Setting up a build](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Setting-up-a-build)
* [Passing build arguments](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Passing-build-arguments)
* [Cross-compiling to a target OS or architecture](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Cross_compiling-to-a-target-OS-or-architecture)
* [Configuring goma](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Configuring-goma)
* [Configuring component mode](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Configuring-component-mode)
* [Step-by-step](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Step_by_step)

* [Adding a build file](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Adding-a-build-file)
* [Testing your addition](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Testing-your-addition)
* [Declaring dependencies](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Declaring-dependencies)
* [Test the static library version](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Test-the-static-library-version)
* [Compiler settings](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Compiler-settings)
* [Putting settings in a config](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Putting-settings-in-a-config)
* [Dependent configs](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Dependent-configs)
* [Add a new build argument](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Add-a-new-build-argument)
* [Dont know whats going on?](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Dont-know-whats-going-on)

* [Print debugging](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Print-debugging)
* [The desc command](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#The-desc-command)
* [Performance](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Performance)


# 运行GN

在正确的配置好depot_tools之后，就可以正常的在命令行中运行GN，gn命令会找到包含当前目录的二进制文件并且运行它

## 设置编译目录

在GYP编译系统中， 系统会在你指定的目录生成`Debug` `Release`目录，但是GN不是这样的，用GN，你可以设置任意的目录作为你的编译目录，当你的编译目录被更新了，相应的ninja文件会自动的重新生成；

指定一个编译目录：

```shell
gn gen out/my_build
```

## 传递编译参数

用下面的命令在你的编译目录生成编译配置参数

```shell
gn args out/my_build
```


这个命令调用一个编辑器让你输入相应的参数; 比如说:

```shell
is_component_build = true
is_debug = false
```


具体的参数你可以通过下面的命令来查询， 看看默认的参数是什么:

```shell
gn args --list out/my_build
```

在上面命令的输出中，请注意查看每个编译参数下面的说明，（⚠️需要说明的是你必须指定编译目录，因为不同的编译目录下可以根据的你的指定产生不同的参数）Chrome的开发者请看一个Chrome特殊的配置说明[Chrome-specific build configuration](http://www.chromium.org/developers/gn-build-configuration)。

## 为一个指定的目标OS和特定的平台（架构）交叉编译

运行 `gn args out/Default` (substituting your build directory as needed)并且指定下面用于交叉编译的一个或多个配置选项；

```shell
target_os = "chromeos"
target_os = "android"

target_cpu = "arm"
target_cpu = "x86"
target_cpu = "x64"
```

具体更详细的信息情查看这片文档 [GNCrossCompiles](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/cross_compiles.md)

## [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Configuring-goma)配置 goma

运行 `gn args out/Default` (substituting your build directory as needed). 添加下面参数：

```shell
use_goma = true
goma_dir = "~/foo/bar/goma"
```

如果你的goma配置在你的默认路径(`~/goma`)，那么你就可以省略`goma_dir`这行配置；

## [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Configuring-component-mode)配置编译的组件（component）模式

这个和上面goma的配置差不多，运行`gn args out/Default`之后，添加：

```shell
is_component_build = true
```
> 这个命令配置的就是静态编译还是动态编译；如果为true的话，就全部是动态库，否则就是静态库

## [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Step_by_step) 手把手教程😃

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Adding-a-build-file) 添加编译文件

创建一个编译文件 `tools/gn/tutorial/BUILD.gn` 并输入如下内容：

```shell
executable("hello_world") {
  sources = [
    "hello_world.cc",
  ]
}
```

这个目录下本身就有一个`hello_world.cc` 文件, 是不是很贴心（containing what you expect）.就是这样的！现在我们需要告诉gn哪个文件需要编译，打开你当前所在的目录src目录中的`BUILD.gn`这个文件并添加这个target到依赖root组的目录下；(一个 “group” 对象是一个元目标，代表着一系列的其他target的集合):

```shell
group("root") {
  deps = [
    ...
    "//url",
    "//tools/gn/tutorial:hello_world",
  ]
}
```

你可以看到你的target是以 “//” (表明这是src目录，src根目录),后面接着是你目录地址后面用冒号':'接着是你的target名字；

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Testing-your-addition)测试你添加的target

在src根目录输入下面命令:

```shell
gn gen out/Default
ninja -C out/Default hello_world
out/Default/hello_world
```

GN的静态编译的target名字不是全局唯一的. 如果你要指定编译具体哪一个目标的时候，你可以在通过ninja编译的时候传递一个target参数给它，同样是“//”＋路径＋目标名字:

```shell
ninja -C out/Default tools/gn/tutorial:hello_world
```

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Declaring-dependencies) 声明依赖关系

下面将的示例中， 我们将编译一个简单的SayHello的静态库例子，在你的目录下会有一个`hello.cc`源文件， 打开`tools/gn/tutorial/BUILD.gn`文件， 将下面的内容加到现有的BUILD.gn中；

<pre class="code">
static_library("hello") {
  sources = [
    "hello.cc",
  ]
}
</pre>

Now let's add an executable that depends on this library:
现在我们加一个依赖这个库的可执行程序；

<pre class="code">
executable("say_hello") {
  sources = [
    "say_hello.cc",
  ]
  deps = [
    ":hello",
  ]
}
</pre>

This executable includes one source file and depends on the previous static library. The static library is referenced by its label in the `deps`. You could have used the full label `//tools/gn/tutorial:hello` but if you're referencing a target in the same build file, you can use the shortcut `:hello`.
这个执行程序包含一个`sya_hello.cc`的源文件，并且这个程序依赖之前我们创建的静态库文件，这个静态库文件是通过关键字`deps`中引入的，这里只是简单的写入了`:hello`来导入这个依赖，我们可以使用全路径来导入依赖， 比如`//tools/gn/tutorial:hello`，如果我们依赖的文件就在当前文件当中， 那么就像上面那样填入名字就好了；

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Test-the-static-library-version)Test the static library version

From the command line in the source root directory:
在src根目录通过命令行来编译和测试我们的程序；

<pre class="code">
ninja -C out/Default say_hello
out/Default/say_hello
</pre>

Note that you **didn't** need to re-run GN. GN will automatically rebuild the ninja files when any build file has changed. You know this happens when ninja prints `[1/1] Regenerating ninja files` at the beginning of execution.
需要注意的是， 我们`不需要` 重新运行GN， 当你的文件有改动的时候GN会自动的重新解析生成ninja文件，你可以通过在编译的时候输出`[1/1] Regenerating ninja files`来判断；

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Compiler-settings)Compiler settings

Our hello library has a new feature, the ability to say hello to two people at once. This feature is controlled by defining `TWO_PEOPLE`. We can add defines like so:
我们的hell库现在有了一个新功能，我们函数调用可以一次sayhello问候两个人，我们想通过宏`TWO_PEOPLE`来控制这个功能， 那么我们可以像下面这样定义：

<pre class="code">
static_library("hello") {
  sources = [
    "hello.cc",
  ]
  defines = [
    "TWO_PEOPLE",
  ]
}
</pre>

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Putting-settings-in-a-config)Putting settings in a config

However, users of the library also need to know about this define, and putting it in the static library target defines it only for the files there. If somebody else includes `hello.h`, they won't see the new definition. To see the new definition, everybody will have to define `TWO_PEOPLE`.
但是， 这个库的使用者也需要知道这个宏的定义，我们将它放在静态库的那个中，那么只能由这个target来使用， 如果其他人引用了头文件`hello.h`,那么这个宏对于他/她来说是不可见的，那么这个功能就是失效了，如果想使用这个功能， 每个引入这个头文件的人都需要重新定义`TWO_PEOPLE`这么一个宏

GN has a concept called a “config” which encapsulates settings. Let's create one that defines our preprocessor define:
GN有一个叫做"config"的概念， 你可以创建一个配置选项来包含所有一系列的设置，我们就来创建一个这样一个配置来处理我们的这个define；

<pre class="code">
config("hello_config") {
  defines = [
    "TWO_PEOPLE",
  ]
}
</pre>

你只需要在config标签上加上这些设置就可以应用到你的目标文件上；
To apply these settings to your target, you only need to add the config's label to the list of configs in the target:

<pre class="code">
static_library("hello") {
  ...
  configs += [
    ":hello_config",
  ]
}
</pre>

Note that you need “+=” here instead of “=” since the build configuration has a default set of configs applied to each target that set up the default build stuff. You want to add to this list rather than overwrite it. To see the default configs, you can use the `print` function in the build file or the `desc` command-line subcommand (see below for examples of both).
注意， 上面我们使用的是+=而不是=，因为我们编译这个target的时候， 其本身就有一些configs， 我们是想增加一些设置而不是取代所有的设置， 想要看所有的default的设置选项，可以在编译文件中使用`print`函数或在命令行中通过`desc`查看， 具体看下面的example；

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Dependent-configs)Dependent configs

This nicely encapsulates our settings, but still requires everybody that uses our library to set the config on themselves. It would be nice if everybody that depends on our `hello` library can get this automatically. Change your library definition to:

<pre class="code">
static_library("hello") {
  sources = [
    "hello.cc",
  ]
  all_dependent_configs = [
    ":hello_config"
  ]
}
</pre>

This applies the `hello_config` to the `hello` target itself, plus all targets that transitively depend on the current one. Now everybody that depends on us will get our settings. You can also set `public_configs` which applies only to targets that directly depend on your target (not transitively).

Now if you compile and run, you'll see the new version with two people:

<pre class="code">
> ninja -C out/Default say_hello
ninja: Entering directory 'out/Default'
[1/1] Regenerating ninja files
[4/4] LINK say_hello
> out/Default/say_hello
Hello, Bill and Joy.
</pre>

## [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Add-a-new-build-argument)Add a new build argument

You declare which arguments you accept and specify default values via `declare_args`.

<pre class="code">
declare_args() {
  enable_teleporter = true
  enable_doom_melon = false
}
</pre>

See `gn help buildargs` for an overview of how this works. See `gn help declare_args` for specifics on declaring them.

It is an error to declare a given argument more than once in a given scope, so care should be used in scoping and naming arguments.

## [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Dont-know-whats-going-on)Don‘t know what’s going on?

You can run GN in verbose mode to see lots of messages about what it's doing. Use `-v` for this.

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Print-debugging)Print debugging

There is a `print` command which just writes to stdout:

<pre class="code">
static_library("hello") {
  ...
  print(configs)
}
</pre>

This will print all of the configs applying to your target (including the default ones).

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#The-desc-command)The “desc” command

You can run `gn desc <build_dir> <targetname>` to get information about a given target:

<pre class="code">
gn desc out/Default //tools/gn/tutorial:say_hello
</pre>

will print out lots of exciting information. You can also print just one section. Lets say you wanted to know where your `TWO_PEOPLE` define came from on the `say_hello` target:

<pre class="code">
> gn desc out/Default //tools/gn/tutorial:say_hello defines --blame
...lots of other stuff omitted...
  From //tools/gn/tutorial:hello_config
       (Added by //tools/gn/tutorial/BUILD.gn:12)
    TWO_PEOPLE
</pre>

You can see that `TWO_PEOPLE` was defined by a config, and you can also see the which line caused that config to be applied to your target (in this case, the `all_dependent_configs` line).

Another particularly interesting variation:

<pre class="code">
gn desc out/Default //base:base_i18n deps --tree
</pre>

See `gn help desc` for more.

### [](https://chromium.googlesource.com/chromium/src/+/master/tools/gn/docs/quick_start.md#Performance)Performance

You can see what took a long time by running it with the --time command line flag. This will output a summary of timings for various things.

You can also make a trace of how the build files were executed:

<pre class="code">
gn --tracelog=mylog.trace
</pre>

and you can load the resulting file in Chrome's `about:tracing` page to look at everything.

<footer class="Site-footer">
    Powered by [Gitiles](https://code.google.com/p/gitiles/)

    [source](https://chromium.googlesource.com/chromium/src/+show/master/tools/gn/docs/quick_start.md)[log](https://chromium.googlesource.com/chromium/src/+log/master/tools/gn/docs/quick_start.md)[blame](https://chromium.googlesource.com/chromium/src/+blame/master/tools/gn/docs/quick_start.md)

