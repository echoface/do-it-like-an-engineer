# Relationship Between View & aura::window

aura::window 里面会通过LayerOwner维护着一个layer， 在`Init()`函数调用的时候创建， 并且通过Setdelegate 将aura::window 作为layer的delegate

webcontent 维护着一个webcontentview的对象，下面是webcontentview的说明命，大致就是这是webcontent具体表现的一个平台的实现， 在aura打开的情况下当然是aura啦....

```
// The WebContentsView is an interface that is implemented by the platform-
// dependent web contents views. The WebContents uses this interface to talk to
// them.
```

webcontentview 里面维护着nativewindow(aura平台的aura::window)nativeview ———aura::window

