# Qt WebChannel Impliment based chromium

在开始介绍之前， 我们先看一段常用的一个应用的一段代码：

```c++
  QWebEnginePage *page = new QWebEnginePage(this);
  ui->webEngineView->setPage(page);
  QWebChannel *channel = new QWebChannel(this);
  channel->registerObject(QStringLiteral("content"), &MsgHandler); //MsgHandler是交互类对象
  page->setWebChannel(channel);
  ui->webEngineView->setUrl(QUrl("you_html_page_uri.html")); //加载一个页面
```

```javascript
<script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
window.onload = function() {          
    new QWebChannel(qt.webChannelTransport, function(channel) {
      var content = channel.objects.content;    //把对象赋值到JS中
      content.updateText("a new msg string");     //updateText 是一个c++中的slot 函数；
    }
//连接QT中发出的信号，里面的message是参数;只需要在QT中调用此函数也就是sendText就可以调用JS函数
  content.sendText.connect(function(message) {
     alert("Received message: " + message);              
  });
}
```

有编程经验的人应该很容易看出来这其中的意思， C++中初始化了一个webengine（qt的web引擎组件已经基于chromium了）将ui组件和WebEngineView和WebEngine绑定， 之后创建了一个QWebChannel对象， 并通过WebChannel对象注册了一个名字为content的对象， 并绑定一个MsgHandler的Qobject的对象用来处理和页面的交互；待会的分析就是从WebEnginePage的`setWebChannel(QwebChannel*)`函数来开始分析， 因为这里是一切的开始；

而在js端， 当页面load完成时， 就可以通过获取这个注册的js对象；有了这个对象，配合Qt 的MetaObject 引入的signal 和 slot机制， 来完成页面的消息传递和函数调用；

当页面初始化的时候，qwebchannel.js会将所有的c++端交互对象的信号和槽在js中生成对应的对象和函数，当c++触发某个信号的时候， 会通过WebChannel内部的一个对象触发一个Chromium的IPC消息， 这个消息以json字符串的形式打包并传送到页面的渲染进程；在render进程收到这个消息的时候，通过调用一个`WebChannelIPCTransport::dispatchWebChannelMessage`函数将这个消息给到V8的运行环境中， 借助于`qwebchannel.js`中的全局对象`qt` 拿到一个js对象中的`webChannelTransport` 对象；通过这个对象的`onmessage`函数，将这个打包好的ipc数据按照一定的格式解析出来，调用到对应的消息处理函数上；

另一方面， 通过在一个创建一个页面的时候， 通过向当前页面注册`webChannelTransport` 这个C++中的包装对象的时候，同样通过google自己实现的一套包装模版函数将c++中WebChannelTransport的成员函数`NativeQtSendMessage`注册为页面中的send函数；这样， 页面也同样可以发送消息给到主进程当中；之后通过qwebchannel类来与应用程序或者对应的QML接口的封装类；

官方另外一个例子是借助于qtwebchannel建立一个简单的websocket server的例子；[see here](http://doc.qt.io/qt-5/qtwebchannel-chatserver-cpp-example.html)

![](/meet_chromium/img/qtwebchannelClassDiagram.png.png)

在Qt包装Webcontents的时候，通过一个Adaptor类WebContentsAdapter来包装整个webcontents必要的接口， 里面提供了下面两个接口：

```c++
QWebChannel *webChannel() const;
void setWebChannel(QWebChannel *, uint worldId);
```

通过这两个接口， 可以向页面注册一个QWebChannel的对象， Adaptor对象通过调用其WebContentsAdapterPrivate对象创建并初始化其webChannelTransport对象；

```c++
void WebContentsAdapter::setWebChannel(QWebChannel *channel, uint worldId) {
    Q_D(WebContentsAdapter);
    if (d->webChannel == channel && d->webChannelWorld == worldId)
        return;
    if (!d->webChannelTransport.get())
        d->webChannelTransport.reset(new WebChannelIPCTransportHost(d->webContents.get(), worldId));
    ...
    d->webChannel = channel;
    d->webChannelWorld = worldId;
    ...
      channel->connectTo(d->webChannelTransport.get());
}
```

当调用`setWebChannel`的时候， 如果没有建立相应的IPC通信类， 就创建一个`WebChannelIPCTransportHost` 对象； 之后将channel和world id保存在webcontntsadapterprivate对象内部， 做为附加在这个页面上的一个channel对象；之后所有的消息、以及映射的信号与槽函数的处理， 都是通过IPC消息转换到channel对象进行处理；在函数最后， 调用了channel的connectTo函数， 将这个IPCtransport 和 channel进行绑定；这个稍后分析， 先来看看`WebChannelIPCTransportHost` 构造函数，其实我们可以想想， 基于chromium这种多进程架构， 如果要与网页环境所在的Render Process建立联系，那么我们必然要通过content API 去setup这个IPC通信环境；

```c++
WebChannelIPCTransportHost::WebChannelIPCTransportHost(content::WebContents *contents, uint worldId, QObject *parent)
    : QWebChannelAbstractTransport(parent)
    , content::WebContentsObserver(contents)
    , m_worldId(worldId)
{
    Send(new WebChannelIPCTransport_Install(routing_id(), m_worldId));
}
```

通过上面的类图可以知道， WebChannelIPCTransportHost类是继承了`QWebChannelAbstractTransport` `content::WebContentsObserver`对象; 实现前者的`sendMessage`函数来向页面发送信号与消息， 后者利用content的接口对象WebContentsObserver来实现chromium多进程之间的ipc消息的发送和接收；在上面的构造函数中， 里面简单的就只有一句话“发送一个Install 的消息给render进程，用来向Render进程的V8执行环境注册安装一些私有函数和全局对象”

```c++
IPC_MESSAGE_HANDLER(WebChannelIPCTransport_Install, installWebChannel)

void WebChannelIPCTransport::installWebChannel(uint worldId)
{
    blink::WebView *webView = render_view()->GetWebView();
    if (!webView)
        return;
    WebChannelTransport::Install(webView->mainFrame(), worldId);
    m_installed = true;
    m_installedWorldId = worldId;
}
```

这里说明一下，WebChannelIPCTransport对象的创建是在render进程中的renderview对象初始化的时候通过content\_render\_client.h 里的接口`RenderViewCreated` 创建的；它继承了RenderViewObserver对象；看到这里应该不难看出， chromium在多进程设计上的一个逻辑对称性； 如果对chromium代码熟悉的同学应该深有感触;  上面的code调用了一个静态函数`WebChannelTransport::Install` 来像V8的context注册一些全局的对象与函数对象；

```c++
void WebChannelTransport::Install(blink::WebFrame *frame, uint worldId)
{
    v8::Isolate *isolate = v8::Isolate::GetCurrent();
    v8::HandleScope handleScope(isolate);
    v8::Handle<v8::Context> context;
    if (worldId == 0)
        context = frame->mainWorldScriptContext();
    else
        context = frame->toWebLocalFrame()->isolatedWorldScriptContext(worldId, 0);
    v8::Context::Scope contextScope(context);

    gin::Handle<WebChannelTransport> transport = gin::CreateHandle(isolate, new WebChannelTransport);
    v8::Handle<v8::Object> global = context->Global();
    v8::Handle<v8::Object> qt = global->Get(gin::StringToV8(isolate, "qt"))->ToObject();
    if (qt.IsEmpty()) {
        qt = v8::Object::New(isolate);
        global->Set(gin::StringToV8(isolate, "qt"), qt);
    }
    qt->Set(gin::StringToV8(isolate, "webChannelTransport"), transport.ToV8());
}
```

最后附上一张整个调用的时序图：

![](/meet_chromium/img/QWebChannelCoreCallSequence.png)

