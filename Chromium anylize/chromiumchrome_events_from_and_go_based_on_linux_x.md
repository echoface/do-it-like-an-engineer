# platform event's "from and go" based on linux X11 system

> chrome 在linux X11上平台事件的生和死


events/platform/x11/x11_event_source_glib.cc
```
GSourceFuncs XSourceFuncs = {
  XSourcePrepare,
  XSourceCheck,
  XSourceDispatch,
  NULL
};
```
通过这样的一个结构体， 并在InitXSource函数中将函数注册给x11系统，将display和事件进行atach的操作；也就是说之后发生在这个display的事件会和这些callback相互联系起来； ~~`在操作系统事件产生的时候调用XSourceDispatch函数`~~
```
gboolean XSourceDispatch(GSource* source,
                         GSourceFunc unused_func,
                         gpointer data) {
  X11EventSource* x11_source = static_cast<X11EventSource*>(data);
  x11_source->DispatchXEvents();
  return TRUE;
}

void X11EventSourceGlib::InitXSource(int fd) {
  DCHECK(!x_source_);
  DCHECK(event_source_.display()) << "Unable to get connection to X server";

  x_poll_.reset(new GPollFD());
  x_poll_->fd = fd;
  x_poll_->events = G_IO_IN;
  x_poll_->revents = 0;

  GLibX11Source* glib_x_source = static_cast<GLibX11Source*>(
      g_source_new(&XSourceFuncs, sizeof(GLibX11Source)));
  glib_x_source->display = event_source_.display();
  glib_x_source->poll_fd = x_poll_.get();

  x_source_ = glib_x_source;
  g_source_add_poll(x_source_, x_poll_.get());
  g_source_set_can_recurse(x_source_, TRUE);
  g_source_set_callback(x_source_, NULL, &event_source_, NULL);
  g_source_attach(x_source_, g_main_context_default());
}
```
InitXSource函数属于X11方面的编程， 没有仔细深究， XSourceDispatch函数中的X11EventSource类的主要功能就像其类申明前面说道的一样
    
    Receives X11 events and sends them to X11EventSourceDelegate. Handles
    receiving, pre-process and post-processing XEvents.
主要就是用来接收X11系统产生的事件，以及做一些相关的预处理以及扫尾工作。其主要几个函数
 - DispatchXEvents()； 
 - ExtractCookieDataDispatchEvent(XEvent* xevent)
 - 维护着一个和事件对应的XDispplay *
 - 还有一个X11EventSourceDelegate* delegate_;对象

```
void X11EventSource::DispatchXEvents() {
  DCHECK(display_);
  // Handle all pending events.
  // It may be useful to eventually align this event dispatch with vsync, but
  // not yet.
  continue_stream_ = true;
  while (XPending(display_) && continue_stream_) {
    XEvent xevent;
    XNextEvent(display_, &xevent);
    ExtractCookieDataDispatchEvent(&xevent);
  }
}
```
这个函数里面即是整个事件循环，函数XNetEvent()等待发生的display 上的相关系统事件；其函数说明：ref：http://www.x.org/archive/X11R7.5/doc/man/man3/XNextEvent.3.html

    The XNextEvent function copies the first event from the event queue into the specified XEvent structure and then removes it from the queue. If the event queue is empty, XNextEvent flushes the output buffer and blocks until an event is received.
当事件发生的时候就填充 xevent变量， 通过函数ExtractCookieDataDispatchEvent将xevent通过X11EventSourceDelegate对象 delegate的ProcessXEvent函数进行传递；
```
void X11EventSource::ExtractCookieDataDispatchEvent(XEvent* xevent) {
  bool have_cookie = false;
  if (xevent->type == GenericEvent &&
      XGetEventData(xevent->xgeneric.display, &xevent->xcookie)) {
    have_cookie = true;
  }
  delegate_->ProcessXEvent(xevent);
  PostDispatchEvent(xevent);
  if (have_cookie)
    XFreeEventData(xevent->xgeneric.display, &xevent->xcookie);
}
```
这里的X11EventSourceDelegate中的函数ProcessXEvent被类X11EventSourceGlib继承并显示，通过，在它的实现中仅仅是调用了其自身的函数DispatchEvent(xevent);来继续分发这个事件；通过查看X11EventSourceGlib类的申明， 瞬间激动了一把， 他不仅继承了X11EventSourceDelegate 还继承了 类PlatformEventSource， 是不是有点感觉了，终于看到了PlatformEventSource，不再是停留在x11 xxx里面了，而是到了我们的google大法里面的platxxx了， 激动！！！
再仔细一看DispatchEvent(xevent)就是~~`重载`~~覆盖（override）的PlatformEventSource的函数；

**好了！ 重点来了~_~; 是不是很激动...不说了，上代码** 
```
uint32_t PlatformEventSource::DispatchEvent(PlatformEvent platform_event) {
  uint32_t action = POST_DISPATCH_PERFORM_DEFAULT;

  FOR_EACH_OBSERVER(PlatformEventObserver, observers_,
                    WillProcessEvent(platform_event));
  // Give the overridden dispatcher a chance to dispatch the event first.
  if (overridden_dispatcher_)
    action = overridden_dispatcher_->DispatchEvent(platform_event);

  if ((action & POST_DISPATCH_PERFORM_DEFAULT) &&
      dispatchers_.might_have_observers()) {
    base::ObserverList<PlatformEventDispatcher>::Iterator iter(&dispatchers_);
    while (PlatformEventDispatcher* dispatcher = iter.GetNext()) {
      if (dispatcher->CanDispatchEvent(platform_event))
        action = dispatcher->DispatchEvent(platform_event);
      if (action & POST_DISPATCH_STOP_PROPAGATION)
        break;
    }
  }
  FOR_EACH_OBSERVER(PlatformEventObserver, observers_,
                    DidProcessEvent(platform_event));

  // If an overridden dispatcher has been destroyed, then the platform
  // event-source should halt dispatching the current stream of events, and wait
  // until the next message-loop iteration for dispatching events. This lets any
  // nested message-loop to unwind correctly and any new dispatchers to receive
  // the correct sequence of events.
  if (overridden_dispatcher_restored_)
    StopCurrentEventStream();

  overridden_dispatcher_restored_ = false;

  return action;
}
```
完了， 半夜了睡觉！
@别急， 快了... 明天继续....

---

看上面code中的这一句
```
if (overridden_dispatcher_)
  action = overridden_dispatcher_->DispatchEvent(platform_event);
    
if ((action & POST_DISPATCH_PERFORM_DEFAULT) &&
  dispatchers_.might_have_observers()) {
    base::ObserverList<PlatformEventDispatcher>::Iterator iter(&dispatchers_);
    while (PlatformEventDispatcher* dispatcher = iter.GetNext()) {
    if (dispatcher->CanDispatchEvent(platform_event))
        action = dispatcher->DispatchEvent(platform_event);
    if (action & POST_DISPATCH_STOP_PROPAGATION)
        break;
    }
}
FOR_EACH_OBSERVER(PlatformEventObserver, observers_,
                  DidProcessEvent(platform_event));
```
定睛一看overridden_dispatcher_成员变量的类型PlatformEventDispatcher* overridden_dispatcher_， PlatformEventDispatcher看上去就是chromium中平台相关的接口，既然到这里，肯定是有某个chromium中的一个类来集成和实现这部分的对接。我检索一下code。
发现继承它的是：
    
    class AURA_EXPORT WindowTreeHostX11 : public WindowTreeHost,
                                          public ui::PlatformEventDispatcher
还有类NativeViewGLSurfaceEGLX11， X11Window， DesktopWindowTreeHostX11，
当然这部分索引出来的都是linux上x11上的一些code， 其实假设我们最后是把他porting到嵌入式平台不带x11的， 可能系统native 窗口是dfbwindow 或者其他的；或者android平台上的Glsurface. 总之我们可以很容一看出来，是chromium的windowtreehost 或要实现类似功能的模块；也就是说：如果我们要全盘托管整个事件的分发， 那么可以通过注册overridden\_dispatcher来获取最高优先级的分发权限；而我们的windowtreehost则是在平台相关的windowtreehost初始化的时候通过`ui::PlatformEventSource::GetInstance()->AddPlatformEventDispatcher(this);`来将自己注册为平台事件的分发者，这样便可以顺利的完成事件的分发；

```
.cc
void PlatformEventSource::AddPlatformEventObserver(
    PlatformEventObserver* observer) {
  CHECK(observer);
  observers_.AddObserver(observer);
}

.h
base::ObserverList<PlatformEventObserver> observers_ 
```
　　整体看来， 整个plat事件分发的时候三个点，一个是平台事件的监听者（platformeventObserver） 一个是用于window_tree 或者 其他平台上的layer tree分发事件的一个重写的platformEventDispatcher（这是正统哦）， 还有通过调用AddPlatformEventDispatcher来分发事件（这个就是那些分封的亲王，襄阳王，平阳王啥的）分别通过他们来将事件传递给想要拿到这些事件的对象。

　　至此， chromium平台事件到此结束。而后面的事件处理就是chromium本身给自己的UI系统也就是基于全新的Aura的子系统分发这些事件， 当让在这个之前，得将这些事件从从PlatEvent 转化成uiEvent， 具体请参见各个继承者对DispatchEvent的具体实现。不同平台拿上来的平台事件也不同有Xevent， 也有windows的 Msg事件 嵌入式平台上也有DFBEvent

一些额外的信息
---

chromium中，PlatformEventDispatcher在分发过程中， 会将事件分发给Chromium内部与平台无关的EventSource对象，在`EventSource::SendEventToProcessor`过程中还提供了一个`EventRewriter` 对象的链表来给我们修改这个平台事件的机会；通过继承EventRewriter相关的接口， 我们可以对我们感兴趣的PlatformEvent进行控制修改；
