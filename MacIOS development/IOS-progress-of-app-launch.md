# 启动过程描述

xcode 开发ios程序帮我们隐藏了太多的东西， 包括系统的初始化，资源的加载，程序的入口等等都帮我们在背后完成了， 如果我们创建single view application， 暴露给我们的就是app的一个delegate 和一个 viewcontroler的入口，

在appdelegate中 我们会得到

* didFinishLaunchingWithOptions
* applicationWillResignActive \/\/由active 状态变成 inactive 时触发
* applicationDidEnterBackground
* applicationWillEnterForeground
* applicationDidBecomeActive
* applicationWillTerminate
* ..... 等等这一系列的消息 我们只要在相应地消息到来的时候做我们想做的事情就好了

而在viewcontroller中， 我们得到的都是界面相关的消息回调。从名字就可以很容易的看出这些函数的意义

* viewDidLoad
* didReceiveMemoryWarning
* .....

ios程序在开始启动时， 内部会帮我们去读取info.plist文件， 里面描述了一些设置，包括安全， 初始化ui的设置，程序名字等等一系列的配置。

##### 修改我们程序第的主界面

1. 我们新建一个storyboard文件
2. 拖入我们想要的界面viewcontroller
3. 在viewcontroller的属性设置栏中，勾选‘is initial view controller’
4. 在info.plist 中选项'Main storyboard file base name' 中填写上正确地文件名字，不需要后缀名

这样你就能修改启动的第一个看到的界面文件了;

#### 修改启动界面

1. 同样在info.plist中我们可以修改‘LaunchScreen storyboard file base name’ 来指定启动界面，例如我们可以在启动过程中，展示一个动画或者一个图片， 来保证用户不是干巴巴的等着我们的程序完全启动！


