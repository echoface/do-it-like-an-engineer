# 为mac上的vim配备代码分析补全工具ycm

人为财死，鸟为食亡，码农折腾升天！

用来写chromium的代码效果图：
![效果图](/IT_Man_Skills/img/YCMPowerVIM.gif)

用习惯了vim 和 ycm， 到哪里都感觉其他东西不爽....

- mac下自带的vim版本不够， 升级，8.0
> brew install macvim

- 使用我私人的vim配置包
```shell
git clone https://github.com/HuanGong/VimConfig
cd VimConfig
./install
# 默认配置包中包含了vundle， 所以只要在vim中使用 `BundInstall`即可将YCM的源码clone到.vim/vundle/YouCompleteMe 目录下
```

- 编译YCMD

 - 安装依赖
 ```shell
  brew install cmake
  #xcode is must
  xcode-select --instal
 ```
 
  - 编译
  > ./install.py --clang-completer --tern-completer # javascript and c/c++
  
  原文教程：最好的教程....
  [Install YCM on macos](https://github.com/Valloric/YouCompleteMe)
  
