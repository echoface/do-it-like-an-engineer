# chromium 在linux平台上与系统输入法对接

chromium 的input作为整个新的Aura UI这部分的基础实现， 他为我们完成了input\_mthod\_base.h类， 在linux平台上， 有`InputMethodAuraLinux` 实现部分负责和输入法对接部分，在Aura的window tree host的实现部分，通过GetInputMethod函数来触发 `input_method_factory.cc` 工厂实现文件来创建不同对应不同平台的实现， 而在`InputMethodAuraLinux`中通过管理LinuxInputMethodContext 来对接不同平台的具体输入法框架，不如说ibus， fcitx...;

LinuxInputMethodContext

```c++
class UI_BASE_IME_EXPORT LinuxInputMethodContext {
public:
      virtual ~LinuxInputMethodContext() {}

      // Dispatches the key event to an underlying IME.  Returns true if the key
      // event is handled, otherwise false.  A client must set the text input type
      // before dispatching a key event.
      virtual bool DispatchKeyEvent(const ui::KeyEvent& key_event) = 0;

      // Tells the system IME for the cursor rect which is relative to the
      // client window rect.
      virtual void SetCursorLocation(const gfx::Rect& rect) = 0;

      // Resets the context.  A client needs to call OnTextInputTypeChanged() again
      // before calling DispatchKeyEvent().
      virtual void Reset() = 0;

      // Focuses the context.
      virtual void Focus() = 0;

      // Blurs the context.
      virtual void Blur() = 0;
};
```

通过这里， 的focus，blur，reset，setcursorLocation DispatchKeyEvent 等几个简单的函数来实现输入法的显示/隐藏、侦听ui事件等等功能； 比如说对应到具体linux平台上，在Focus函数中，可调用gtk的 `gtk_im_context_focus_in(gtk_context_);`函数来call其系统平台的键盘；

当然， 我们也能在这里通过继承来实现自己的一套只为chromium使用的键盘..

