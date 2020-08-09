#Aura::Window 与 ToolKit Webview是什么一样的关系

在chromium中，Toolkit是基于Aura来做的， aura是为了解决统一绘制，跨平台，在高低端平台上的性能上的灵活性，还包括shell环境和窗口管理已经硬件加速等等一些列目标而在chromium中引入了aura project； 而在aura project中，基于这样的一个基础上利用skia｛小巧高效｝绘制技术开发的称之为views的UI Framework组件， 基于