# Web IDL on chromium

下面两个是chromium项目中关于对webidl（web interface definition language）一些说明

* [webidl](https://www.chromium.org/blink/webidl)
* [web-idl-interfaces](https://www.chromium.org/developers/web-idl-interfaces)

** 在idl中描述的属性和方法一定要按照规则编写，不然的话很容易出错**
正常情况下binding成功之后， 会在`/out/Release/gen/blink/bindings/core/v8/V8[IDL名称].cpp[h]` 生成相应binding的`C/C++`的实现。

LocalFram
通过`client()`可以访问`FrameClient`
FrameClient()里通过`page()`拿到`chromeClient`
  `page()->chromeClient()`

```
WebLocalFrameImpl* webframe = WebLocalFrameImpl::fromFrame(frame);
if (webframe->client()) {
    if (WebUserGestureIndicator::isProcessingUserGesture())
        WebUserGestureIndicator::currentUserGestureToken().setJavascriptPrompt();
    webframe->client()->runModalAlertDialog(message);
    return true;
}
```

