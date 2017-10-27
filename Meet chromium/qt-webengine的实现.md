# Qt wenegine的实现结构

QTWebengine的实现大致分成了三个大的部分:

1. `blink/webkit`端，通过动态的方法在一个网页创建的时候，通过继承renderviewobserver的renderviewcreated方法中向v8的执行上下文中注册webChannelTransport对象用来支持qtwenchannel的机制（一个html页面可以和nativec＋＋和qml环境通信机制的实现）；同时通过继承`ContentRenderClient`对象，override `RunScriptsAtDocumentStart[End]`等方法注册入一个qt_webengine.js代码， 这是一个简单的js框架， 他对通过v8方法注册进去的webChannelTransport对象进行了js方法封装和函数的支持；

2. 基于chromium content成的代码实现了qt自己的`shell`; 成实现了对webcontent 的包装和绘制的对接，简单的说就是仿照`chromium/src/content/shell`下shell的实现，围绕webcontent，实现了一个最小浏览器，其中重要的一部分就是通过用qt的图形合成代替了aura对接的一部分,通过继承`content::RenderWidgetHostViewBase`来负责将绘制好的页面通过`OnSwapCompositorFrame`函数将数据合成到qt的图形当中；同时在这个`shell`中，实现了一系列的delegate和adaptor，将content browser端的相关代码桥接到qt的系统当中；当网页绘制好，数据通过sharememory更新到browser端的renderwidegethostviewQT对象中，调用相关的adaptor的代码将数据update到qt中， 系统发生的事件， 由Qwidget说代表的window接收到之后， 同样通过adaptor层转换传递到RenderWidgetHostViewQT中，再由它通过IPC发送到Render进程来完成交互；

3. 第三部分就是qt自己的实现了， 在第二部分当中， 通过一系列的adaptor和delegate的接口， 导出了一些列必要的设置和操作，最后，利用这些接口实现了qt的两部分的组件， 一个用于传统C＋＋编程的widget组件，一个是export到qml运行环境的quick组件；


比如说一个css动画触发的绘制，当绘制完成Chromium render进程会发送IPC消息到Browser这边；在RenderWidgetHostViewQt对象中通过复写`virtual void OnSwapCompositorFrame(uint32_t output_surface_id, scoped_ptr<cc::CompositorFrame> frame)函数， 在函数中触发qtquickitem【QML】或者qtwebenginewidget【QTWIDGET】对象的update；update函数就是安排重绘；`

### void QQuickItem::update\(\)

Schedules a call to [updatePaintNode](http://doc.qt.io/qt-5/qquickitem.html#updatePaintNode)\(\) for this item.

The call to [QQuickItem::updatePaintNode](http://doc.qt.io/qt-5/qquickitem.html#updatePaintNode)\(\) will always happen if the item is showing in a [QQuickWindow](http://doc.qt.io/qt-5/qquickwindow.html).

Only items which specify [QQuickItem::ItemHasContents](http://doc.qt.io/qt-5/qquickitem.html#Flag-enum) are allowed to call QQuickItem::update\(\).

在重绘函数`updatePaintNode中将冲render中交换回来的数据对象ChromiumCompositorData通过DelegatedFrameNode::commit完成数据的交换，经过commit函数，所有chromium绘制的数据都交换到了QSGNode对象中；QSGNode在updatePaintNode中返回给qt的绘制系统，与qtwidget/qtquickitem对象继续合成并显示；`

上面的ChromiumCompositorData对象是对QSharedData的封装；里面并维护着chromium中真正的数据对象`scoped_ptr<cc::DelegatedFrameData> frameData;`

## 加班累到爆，整理中......



