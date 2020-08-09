# Chromium_input_type_change_call_stack

前几天遇到个问题， 导致在我们的浏览器上，焦点无缘无故的丢失了，导致到content层时导致输入状态不对，从而使得软键盘输入无效的问题；所以就稍微将这部分代码看了一下，webkit里面焦点变化主要是由下面几种情况引起的；
###主要三种情况
- html element focus change by keyevent or js's Set active elements
- pepper plugin set focus
- mouse select event for editor
---

### Mouse selection Event
```
void EditorClientImpl::respondToChangedSelection(LocalFrame* frame, SelectionType selectionType)
{
    WebLocalFrameImpl* webFrame = WebLocalFrameImpl::fromFrame(frame);
    if (webFrame->client())
        webFrame->client()->didChangeSelection(selectionType != RangeSelection);
}

virtual void didChangeSelection(bool isSelectionEmpty) { }
//override by render_frame
```


## Html element Focus
```
void Element::focus(const FocusParams& params)
    call: document().page()->chromeClient().showImeIfNeeded();

void ChromeClientImpl::showImeIfNeeded()
    call: if (m_webView->client())
            m_webView->client()->showImeIfNeeded();
        

void RenderWidget::showImeIfNeeded():
// override src/third_party/WebKit/public/web/WebWidgetClient.h	
    call: OnShowImeIfNeeded();

void RenderWidget::OnShowImeIfNeeded()
    Call: UpdateTextInputState
    
void RenderWidget::UpdateTextInputState(ShowIme show_ime,
                        ChangeSource change_source)
    set: text_input_type_ = new_type;
```






