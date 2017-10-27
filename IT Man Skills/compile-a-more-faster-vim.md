# Compile A More Faster Vim For Myself

因为工作中都是用的Vim， 而自己习惯了VIM + YCM这样的一套简单的组合，而悲剧的是公司服务器上因为加密和外网访问等等限制没法使用`apt install`； 自带的vim不仅仅版本过低， 功能不全之外还有很多因为`加密`带来的副作用，比如说，竟然限制vim的yy只能在99字符以内｛ps: 鄙视，让不让人写代码｝；被逼无奈，虽然自己私下已经破解了这个所谓的`加密`,但是也只是个演示的程序； 所以只能自己Compile一份放在自己的$HOME；

因为我使用的环境中没有GUI， 所以GUI的支持没有意义， 而基本上自己使用的就是一些基本vim插件和YCM这个神器；所以很多功能没有必要开启； 在通过`vim --startuptime`启动时间分析发现选项`-xterm_clipboard`严重影响启动； 于是我用下面的命令编译了一个没有GUI、clipboard、X11的Huge版本， 这样速度提升十分明显；
shell cmd:
```
./configure  --prefix=$HOME  --with-features=huge --enable-pythoninterp=yes  --enable-cscope --enable-fail-if-missing --enable-multibyte --enable-fontset --with-compiledby="HuanGong" --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/ --disable-gui --without-x
```
需要GUI和X11支持的,去掉开关`disable-gui --withou-x`就可以了，不过这样编译出来就回带有系统剪切板的支持；具体机器和使用环境最好的办法还是通过`--startuptime`分析来得到一个结果，之后根据自己的情况针对性的解决；
