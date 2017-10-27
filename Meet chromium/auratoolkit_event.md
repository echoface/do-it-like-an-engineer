# Aura\_Toolkit\_Event

这是一份v39上的chromium在x11平台上的事件的backtrace，这时候的事件分发其实还是比较乱的，从V32开始引入新的AURA以来， 改动比较大，新一点的v47 v52上面整理的改进之后，这一部分变得简单多了；

在最新的v53上， 系统=&gt;WindowTreehost=&gt;InputMethod=&gt;EventDispatcher=&gt;EventTarget=&gt;EventHnadler

到AURA TOOLKIT UI的:

```
(gdb) bt
#0  views::Textfield::OnKeyPressed (this=0x3f3e3a82c520, event=...)
    at ../../ui/views/controls/textfield/textfield.cc:669
#1  0x00000000049fee13 in views::View::OnKeyEvent (this=0x3f3e3a82c520, event=0x3f3e3b91e420)
    at ../../ui/views/view.cc:960
#2  0x00000000049fee8f in non-virtual thunk to views::View::OnKeyEvent(ui::KeyEvent*) () at ../../ui/views/view.cc:964
#3  0x00000000013c5465 in ui::EventHandler::OnEvent (this=0x3f3e3a82c550, event=0x3f3e3b91e420)
    at ../../ui/events/event_handler.cc:27
#4  0x00000000013c697e in ui::EventTarget::OnEvent (this=0x3f3e3a82c550, event=0x3f3e3b91e420)
    at ../../ui/events/event_target.cc:64
#5  0x00000000013ceee2 in ui::EventDispatcher::DispatchEvent (this=0x7fffffff6d28, handler=0x3f3e3a82c550,
    event=0x3f3e3b91e420) at ../../ui/events/event_dispatcher.cc:189
#6  0x00000000013ce7ea in ui::EventDispatcher::ProcessEvent (this=0x7fffffff6d28, target=0x3f3e3a82c550,
    event=0x3f3e3b91e420) at ../../ui/events/event_dispatcher.cc:137
#7  0x00000000013ce578 in ui::EventDispatcherDelegate::DispatchEventToTarget (this=0x3f3e3a5e3ad8,
    target=0x3f3e3a82c550, event=0x3f3e3b91e420) at ../../ui/events/event_dispatcher.cc:85
#8  0x00000000013ce452 in ui::EventDispatcherDelegate::DispatchEvent (this=0x3f3e3a5e3ad8, target=0x3f3e3a82c550,
    event=0x3f3e3b91e420) at ../../ui/events/event_dispatcher.cc:57
#9  0x0000000004db5d4e in ui::EventProcessor::OnEventFromSource (this=0x3f3e3a5e3ad8, event=0x7fffffff8cf8)
    at ../../ui/events/event_processor.cc:32
#10 0x0000000004a551fd in views::internal::RootView::OnEventFromSource (this=0x3f3e3a5e38a0, event=0x7fffffff8cf8)
    at ../../ui/views/widget/root_view.cc:254
#11 0x0000000004a554bf in non-virtual thunk to views::internal::RootView::OnEventFromSource(ui::Event*) ()
    at ../../ui/views/widget/root_view.cc:301
#12 0x0000000004db6a04 in ui::EventSource::DeliverEventToProcessor (this=0x3f3e3a7c2fe8, event=0x7fffffff8cf8)
    at ../../ui/events/event_source.cc:73
#13 0x0000000004db6682 in ui::EventSource::SendEventToProcessor (this=0x3f3e3a7c2fe8, event=0x7fffffff8cf8)
    at ../../ui/events/event_source.cc:51
#14 0x0000000004a14f2f in views::Widget::OnKeyEvent (this=0x3f3e3a7c2fe0, event=0x7fffffff8cf8)
    at ../../ui/views/widget/widget.cc:1186
#15 0x0000000004a8bb4e in views::DesktopNativeWidgetAura::OnKeyEvent (this=0x3f3e3a793420, event=0x7fffffff8cf8)
    at ../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:1029
#16 0x0000000004a8bbff in non-virtual thunk to views::DesktopNativeWidgetAura::OnKeyEvent(ui::KeyEvent*) ()
    at ../../ui/views/widget/desktop_aura/desktop_native_widget_aura.cc:1036
#17 0x00000000013c5465 in ui::EventHandler::OnEvent (this=0x3f3e3a793428, event=0x7fffffff8cf8)
    at ../../ui/events/event_handler.cc:27
#18 0x00000000013c6966 in ui::EventTarget::OnEvent (this=0x3f3e3a676908, event=0x7fffffff8cf8)
    at ../../ui/events/event_target.cc:62
#19 0x00000000013ceee2 in ui::EventDispatcher::DispatchEvent (this=0x7fffffff84e8, handler=0x3f3e3a676908,
    event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:189
---Type <return> to continue, or q <return> to quit---
#20 0x00000000013ce7ea in ui::EventDispatcher::ProcessEvent (this=0x7fffffff84e8, target=0x3f3e3a676908,
    event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:137
#21 0x00000000013ce578 in ui::EventDispatcherDelegate::DispatchEventToTarget (this=0x3f3e3a72a6e0,
    target=0x3f3e3a676908, event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:85
#22 0x00000000013ce452 in ui::EventDispatcherDelegate::DispatchEvent (this=0x3f3e3a72a6e0, target=0x3f3e3a676908,
    event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:57
#23 0x0000000004db5d4e in ui::EventProcessor::OnEventFromSource (this=0x3f3e3a72a6e0, event=0x7fffffff8cf8)
    at ../../ui/events/event_processor.cc:32
#24 0x0000000005e6c596 in wm::InputMethodEventFilter::DispatchKeyEventPostIME (this=0x3f3e3a8ca920, event=...)
    at ../../ui/wm/core/input_method_event_filter.cc:100
#25 0x0000000005e6c6cf in non-virtual thunk to wm::InputMethodEventFilter::DispatchKeyEventPostIME(ui::KeyEvent const&)
    () at ../../ui/wm/core/input_method_event_filter.cc:103
#26 0x00000000013b6cc7 in ui::InputMethodBase::DispatchKeyEventPostIME (this=0x3f3e3a8ca9e0, event=...)
    at ../../ui/base/ime/input_method_base.cc:119
#27 0x00000000013b5b2f in ui::InputMethodAuraLinux::DispatchKeyEvent (this=0x3f3e3a8ca9e0, event=...)
    at ../../ui/base/ime/input_method_auralinux.cc:69
#28 0x0000000005e6c408 in wm::InputMethodEventFilter::OnKeyEvent (this=0x3f3e3a8ca920, event=0x7fffffffc3a8)
    at ../../ui/wm/core/input_method_event_filter.cc:66
#29 0x0000000005e60c72 in wm::CompoundEventFilter::FilterKeyEvent (this=0x3f3e3a7b1420, event=0x7fffffffc3a8)
    at ../../ui/wm/core/compound_event_filter.cc:136
#30 0x0000000005e60ff3 in wm::CompoundEventFilter::OnKeyEvent (this=0x3f3e3a7b1420, event=0x7fffffffc3a8)
    at ../../ui/wm/core/compound_event_filter.cc:201
#31 0x00000000013c5465 in ui::EventHandler::OnEvent (this=0x3f3e3a7b1420, event=0x7fffffffc3a8)
    at ../../ui/events/event_handler.cc:27
#32 0x00000000013ceee2 in ui::EventDispatcher::DispatchEvent (this=0x7fffffff9788, handler=0x3f3e3a7b1420,
    event=0x7fffffffc3a8) at ../../ui/events/event_dispatcher.cc:189
#33 0x00000000013cec84 in ui::EventDispatcher::DispatchEventToEventHandlers (this=0x7fffffff9788, list=0x7fffffff97a0,
    event=0x7fffffffc3a8) at ../../ui/events/event_dispatcher.cc:168
#34 0x00000000013ce766 in ui::EventDispatcher::ProcessEvent (this=0x7fffffff9788, target=0x3f3e3a676908,
    event=0x7fffffffc3a8) at ../../ui/events/event_dispatcher.cc:126
#35 0x00000000013ce578 in ui::EventDispatcherDelegate::DispatchEventToTarget (this=0x3f3e3a72a6e0,
    target=0x3f3e3a676908, event=0x7fffffffc3a8) at ../../ui/events/event_dispatcher.cc:85
#36 0x00000000013ce452 in ui::EventDispatcherDelegate::DispatchEvent (this=0x3f3e3a72a6e0, target=0x3f3e3a676908,
    event=0x7fffffffc3a8) at ../../ui/events/event_dispatcher.cc:57
#37 0x0000000004db5d4e in ui::EventProcessor::OnEventFromSource (this=0x3f3e3a72a6e0, event=0x7fffffffc3a8)
    at ../../ui/events/event_processor.cc:32
#38 0x0000000004db6a04 in ui::EventSource::DeliverEventToProcessor (this=0x3f3e3a5e2b38, event=0x7fffffffc3a8)
    at ../../ui/events/event_source.cc:73
#39 0x0000000004db6682 in ui::EventSource::SendEventToProcessor (this=0x3f3e3a5e2b38, event=0x7fffffffc3a8)
---Type <return> to continue, or q <return> to quit---
    at ../../ui/events/event_source.cc:51
#40 0x0000000004a6ab31 in views::DesktopWindowTreeHostX11::DispatchEvent (this=0x3f3e3a5e2aa0,
    event=@0x7fffffffc790: 0x7fffffffc7f8) at ../../ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:1672
#41 0x0000000004a6bfdf in non-virtual thunk to views::DesktopWindowTreeHostX11::DispatchEvent(_XEvent* const&) ()
    at ../../ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:1916
#42 0x0000000004dde023 in ui::PlatformEventSource::DispatchEvent (this=0x3f3e3a5e6a40, platform_event=0x7fffffffc7f8)
    at ../../ui/events/platform/platform_event_source.cc:79
#43 0x0000000004de543f in ui::X11EventSource::DispatchEvent (this=0x3f3e3a5e6a40, xevent=0x7fffffffc7f8)
    at ../../ui/events/platform/x11/x11_event_source.cc:142
#44 0x0000000004de534b in ui::X11EventSource::DispatchXEvents (this=0x3f3e3a5e6a40)
    at ../../ui/events/platform/x11/x11_event_source.cc:118
#45 0x0000000004de5c25 in ui::(anonymous namespace)::XSourceDispatch (source=0x3f3e3a55f860, unused_func=0x0,
    data=0x3f3e3a5e6a40) at ../../ui/events/platform/x11/x11_event_source_glib.cc:39
#46 0x00007ffff70b7ce5 in g_main_dispatch (context=0x3f3e3a59da70) at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3064
#47 g_main_context_dispatch (context=context@entry=0x3f3e3a59da70) at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3663
#48 0x00007ffff70b8048 in g_main_context_iterate (context=context@entry=0x3f3e3a59da70, block=block@entry=1,
    dispatch=dispatch@entry=1, self=<optimized out>) at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3734
#49 0x00007ffff70b80ec in g_main_context_iteration (context=0x3f3e3a59da70, may_block=1)
    at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3795
#50 0x0000000000787105 in base::MessagePumpGlib::Run (this=0x3f3e3a55f180, delegate=0x3f3e3a6516a0)
    at ../../base/message_loop/message_pump_glib.cc:309
#51 0x00000000006ee1e0 in base::MessageLoop::RunHandler (this=0x3f3e3a6516a0)
    at ../../base/message_loop/message_loop.cc:415
#52 0x000000000071f44b in base::RunLoop::Run (this=0x7fffffffce20) at ../../base/run_loop.cc:54
#53 0x0000000003c68e00 in content::BrowserMainLoop::MainMessageLoopRun (this=0x3f3e3a618e20)
    at ../../content/browser/browser_main_loop.cc:1151
#54 0x0000000003c68ca1 in content::BrowserMainLoop::RunMainMessageLoopParts (this=0x3f3e3a618e20)
    at ../../content/browser/browser_main_loop.cc:753
#55 0x00000000038ce217 in content::BrowserMainRunnerImpl::Run (this=0x3f3e3a6130e0)
    at ../../content/browser/browser_main_runner.cc:205
#56 0x0000000000434249 in ShellBrowserMain (parameters=..., main_runner=...)
    at ../../content/shell/browser/shell_browser_main.cc:226
#57 0x0000000000431c28 in content::ShellMainDelegate::RunProcess (this=0x7fffffffe400, process_type=...,
    main_function_params=...) at ../../content/shell/app/shell_main_delegate.cc:250
#58 0x00000000005112b3 in content::RunNamedProcessTypeMain (process_type=..., main_function_params=..., delegate=
    0x7fffffffe400) at ../../content/app/content_main_runner.cc:407
#59 0x00000000005133d8 in content::ContentMainRunnerImpl::Run (this=0x3f3e3a59b380)
    at ../../content/app/content_main_runner.cc:769
#60 0x0000000000510975 in content::ContentMain (params=...) at ../../content/app/content_main.cc:19
#61 0x0000000000430e3c in main (argc=5, argv=0x7fffffffe538) at ../../content/shell/app/shell_main.cc:49
```

到页面的：

```sh
(gdb) bt
#0  content::RenderWidgetHostViewAura::OnKeyEvent (this=0x2805d183020, event=0x7fffffff8cf8)
    at ../../content/browser/renderer_host/render_widget_host_view_aura.cc:1818
#1  0x0000000003a4f36f in non-virtual thunk to content::RenderWidgetHostViewAura::OnKeyEvent(ui::KeyEvent*) ()
    at ../../content/browser/renderer_host/render_widget_host_view_aura.cc:1875
#2  0x00000000013c5465 in ui::EventHandler::OnEvent (this=0x2805d183108, event=0x7fffffff8cf8)
    at ../../ui/events/event_handler.cc:27
#3  0x00000000013c6966 in ui::EventTarget::OnEvent (this=0x2805d0d2388, event=0x7fffffff8cf8)
    at ../../ui/events/event_target.cc:62
#4  0x00000000013ceee2 in ui::EventDispatcher::DispatchEvent (this=0x7fffffff84e8, handler=0x2805d0d2388,
    event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:189
#5  0x00000000013ce7ea in ui::EventDispatcher::ProcessEvent (this=0x7fffffff84e8, target=0x2805d0d2388,
    event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:137
#6  0x00000000013ce578 in ui::EventDispatcherDelegate::DispatchEventToTarget (this=0x2805ce1c6e0,
    target=0x2805d0d2388, event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:85
#7  0x00000000013ce452 in ui::EventDispatcherDelegate::DispatchEvent (this=0x2805ce1c6e0, target=0x2805d0d2388,
    event=0x7fffffff8cf8) at ../../ui/events/event_dispatcher.cc:57
#8  0x0000000004db5d4e in ui::EventProcessor::OnEventFromSource (this=0x2805ce1c6e0, event=0x7fffffff8cf8)
    at ../../ui/events/event_processor.cc:32
#9  0x0000000005e6c596 in wm::InputMethodEventFilter::DispatchKeyEventPostIME (this=0x2805cf98ce0, event=...)
    at ../../ui/wm/core/input_method_event_filter.cc:100
#10 0x0000000005e6c6cf in non-virtual thunk to wm::InputMethodEventFilter::DispatchKeyEventPostIME(ui::KeyEvent const&)
    () at ../../ui/wm/core/input_method_event_filter.cc:103
#11 0x00000000013b6cc7 in ui::InputMethodBase::DispatchKeyEventPostIME (this=0x2805cecb4a0, event=...)
    at ../../ui/base/ime/input_method_base.cc:119
#12 0x00000000013b5b2f in ui::InputMethodAuraLinux::DispatchKeyEvent (this=0x2805cecb4a0, event=...)
    at ../../ui/base/ime/input_method_auralinux.cc:69
#13 0x0000000005e6c408 in wm::InputMethodEventFilter::OnKeyEvent (this=0x2805cf98ce0, event=0x7fffffffc218)
    at ../../ui/wm/core/input_method_event_filter.cc:66
#14 0x0000000005e60c72 in wm::CompoundEventFilter::FilterKeyEvent (this=0x2805ceb0520, event=0x7fffffffc218)
    at ../../ui/wm/core/compound_event_filter.cc:136
#15 0x0000000005e60ff3 in wm::CompoundEventFilter::OnKeyEvent (this=0x2805ceb0520, event=0x7fffffffc218)
    at ../../ui/wm/core/compound_event_filter.cc:201
#16 0x00000000013c5465 in ui::EventHandler::OnEvent (this=0x2805ceb0520, event=0x7fffffffc218)
    at ../../ui/events/event_handler.cc:27
#17 0x00000000013ceee2 in ui::EventDispatcher::DispatchEvent (this=0x7fffffff9788, handler=0x2805ceb0520,
    event=0x7fffffffc218) at ../../ui/events/event_dispatcher.cc:189
#18 0x00000000013cec84 in ui::EventDispatcher::DispatchEventToEventHandlers (this=0x7fffffff9788, list=0x7fffffff97a0,
    event=0x7fffffffc218) at ../../ui/events/event_dispatcher.cc:168
#19 0x00000000013ce766 in ui::EventDispatcher::ProcessEvent (this=0x7fffffff9788, target=0x2805d0d2388,
---Type <return> to continue, or q <return> to quit---
    event=0x7fffffffc218) at ../../ui/events/event_dispatcher.cc:126
#20 0x00000000013ce578 in ui::EventDispatcherDelegate::DispatchEventToTarget (this=0x2805ce1c6e0,
    target=0x2805d0d2388, event=0x7fffffffc218) at ../../ui/events/event_dispatcher.cc:85
#21 0x00000000013ce452 in ui::EventDispatcherDelegate::DispatchEvent (this=0x2805ce1c6e0, target=0x2805d0d2388,
    event=0x7fffffffc218) at ../../ui/events/event_dispatcher.cc:57
#22 0x0000000004db5d4e in ui::EventProcessor::OnEventFromSource (this=0x2805ce1c6e0, event=0x7fffffffc218)
    at ../../ui/events/event_processor.cc:32
#23 0x0000000004db6a04 in ui::EventSource::DeliverEventToProcessor (this=0x2805ccd5b38, event=0x7fffffffc218)
    at ../../ui/events/event_source.cc:73
#24 0x0000000004db6682 in ui::EventSource::SendEventToProcessor (this=0x2805ccd5b38, event=0x7fffffffc218)
    at ../../ui/events/event_source.cc:51
#25 0x0000000004a6abbb in views::DesktopWindowTreeHostX11::DispatchEvent (this=0x2805ccd5aa0,
    event=@0x7fffffffc790: 0x7fffffffc7f8) at ../../ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:1683
#26 0x0000000004a6bfdf in non-virtual thunk to views::DesktopWindowTreeHostX11::DispatchEvent(_XEvent* const&) ()
    at ../../ui/views/widget/desktop_aura/desktop_window_tree_host_x11.cc:1916
#27 0x0000000004dde023 in ui::PlatformEventSource::DispatchEvent (this=0x2805ccd9a40, platform_event=0x7fffffffc7f8)
    at ../../ui/events/platform/platform_event_source.cc:79
#28 0x0000000004de543f in ui::X11EventSource::DispatchEvent (this=0x2805ccd9a40, xevent=0x7fffffffc7f8)
    at ../../ui/events/platform/x11/x11_event_source.cc:142
#29 0x0000000004de534b in ui::X11EventSource::DispatchXEvents (this=0x2805ccd9a40)
    at ../../ui/events/platform/x11/x11_event_source.cc:118
#30 0x0000000004de5c25 in ui::(anonymous namespace)::XSourceDispatch (source=0x2805cc52860, unused_func=0x0,
    data=0x2805ccd9a40) at ../../ui/events/platform/x11/x11_event_source_glib.cc:39
#31 0x00007ffff70b7ce5 in g_main_dispatch (context=0x2805cc90a70) at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3064
#32 g_main_context_dispatch (context=context@entry=0x2805cc90a70) at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3663
#33 0x00007ffff70b8048 in g_main_context_iterate (context=context@entry=0x2805cc90a70, block=block@entry=1,
    dispatch=dispatch@entry=1, self=<optimized out>) at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3734
#34 0x00007ffff70b80ec in g_main_context_iteration (context=0x2805cc90a70, may_block=1)
    at /build/buildd/glib2.0-2.40.2/./glib/gmain.c:3795
#35 0x0000000000787105 in base::MessagePumpGlib::Run (this=0x2805cc52180, delegate=0x2805cd416a0)
    at ../../base/message_loop/message_pump_glib.cc:309
#36 0x00000000006ee1e0 in base::MessageLoop::RunHandler (this=0x2805cd416a0)
    at ../../base/message_loop/message_loop.cc:415
#37 0x000000000071f44b in base::RunLoop::Run (this=0x7fffffffce20) at ../../base/run_loop.cc:54
#38 0x0000000003c68e00 in content::BrowserMainLoop::MainMessageLoopRun (this=0x2805ccfae20)
    at ../../content/browser/browser_main_loop.cc:1151
#39 0x0000000003c68ca1 in content::BrowserMainLoop::RunMainMessageLoopParts (this=0x2805ccfae20)
    at ../../content/browser/browser_main_loop.cc:753
#40 0x00000000038ce217 in content::BrowserMainRunnerImpl::Run (this=0x2805ccf5f80)
---Type <return> to continue, or q <return> to quit---
    at ../../content/browser/browser_main_runner.cc:205
#41 0x0000000000434249 in ShellBrowserMain (parameters=..., main_runner=...)
    at ../../content/shell/browser/shell_browser_main.cc:226
#42 0x0000000000431c28 in content::ShellMainDelegate::RunProcess (this=0x7fffffffe400, process_type=...,
    main_function_params=...) at ../../content/shell/app/shell_main_delegate.cc:250
#43 0x00000000005112b3 in content::RunNamedProcessTypeMain (process_type=..., main_function_params=...,
    delegate=0x7fffffffe400) at ../../content/app/content_main_runner.cc:407
#44 0x00000000005133d8 in content::ContentMainRunnerImpl::Run (this=0x2805cc8e380)
    at ../../content/app/content_main_runner.cc:769
#45 0x0000000000510975 in content::ContentMain (params=...) at ../../content/app/content_main.cc:19
#46 0x0000000000430e3c in main (argc=5, argv=0x7fffffffe538) at ../../content/shell/app/shell_main.cc:49



```

