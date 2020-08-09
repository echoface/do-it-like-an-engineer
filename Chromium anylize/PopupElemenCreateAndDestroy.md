# popup元素的创建和销毁


##摘要：
    blink::WebWidgetClient   blink::webpagePopup : public WebWidget
    RenderWidget: 内部提供了静态函数 Create，根据 blink::WebPopupType 创建不同的renderwidget，renderviewImpl 内部创建的 
    
    WebViewClient : virtual public WebWidgetClient
    WebWidgetClient <-----> RenderViewImpl ：public blink::WebViewClient ，
                                         RenderView,
                                         RenderWidget,
                                         RenderWidget,
                                         blink::WebWidgetClient 

---

    domtree 中有各种obj pop类的就有 windowpagepopup， DateTimeChooserImpl.h， PopupMenuImpl.h	

##create [创建过程]：

Source/core/html/HTMLSelectElement.cpp
```
blink::HTMLSelectElement::defaultEventHandler
	blink::HTMLSelectElement::menuListDefaultEventHandler
		blink::RenderMenuList::showPopup
```
Source/core/rendering/RenderMenuList.cpp
```
	blink::RenderMenuList::showPopup
		m_popup->show(quad, size, select->optionToListIndex(select->selectedIndex()));
```
Source/web/PopupMenuChromium.cpp
```
PopupMenuChromium::show(const FloatQuad& controlPosition, const IntSize& controlSize, int index)
		m_popup->showInRect(controlPosition, controlSize, m_frameView.get(), index);
```
Source/web/PopupContainer.cpp:419
```
PopupContainer::showInRect(const FloatQuad& controlPosition, const IntSize& controlSize, FrameView* v, int index)
		showPopup(v);
PopupContainer::showPopup(FrameView* view)
		popupOpened(layoutAndCalculateWidgetRect(m_controlSize.height(), transformOffset, roundedIntPoint(m_controlPosition.p4())));
PopupContainer::popupOpened(const IntRect& bounds)
		WebWidget* webwidget = webView->client()->createPopupMenu(WebPopupTypeSelect);
		toWebPopupMenuImpl(webwidget)->initialize(this, bounds);
```
Source/web/WebViewImpl.cpp
```
WebViewImpl::openPagePopup(PagePopupClient* client)
		WebWidget* popupWidget = m_client->createPopupMenu(WebPopupTypePage);   ps：wekit中WebViewClient.h ----> content中 RenderViewImpl
		m_pagePopup->initialize(this, client)
```
Source/web/WebPagePopupImpl.cpp ： public PagePopup
	void WebPopupMenuImpl::initialize(PopupContainer* widget, const WebRect& bounds)
		m_client->setWindowRect(bounds);
		m_client->show(WebNavigationPolicy()); //invoke it   --------------- RenderWidget

./sraf_porting/content/renderer/render_widget.cc
```
RenderWidget::show(WebNavigationPolicy)   ps：RenderWidget :public blink::WebWidgetClient
	f： Send(new ViewHostMsg_ShowWidget(opener_id_, routing_id_, initial_pos_))
```
sraf_porting/content/browser/renderer_host/render_view_host_impl.cc
```
IPC_MESSAGE_HANDLER(ViewHostMsg_ShowWidget, OnShowWidget)
OnShowWidget(int route_id, gfx::rect inital_pos)
	f:  delegate_->ShowCreatedWidget(route_id, initial_pos);

web_content_impl
	f：WebContentsImpl::ShowCreatedWidget
		widget_host_view = GetCreatedWidget(route_id)
		view = GetRenderWidgetHostView()
		f：widget_host_view->InitAsChild(GetRenderWidgetHostView()->GetNativeView()); ||
		   widget_host_view->InitAsFullscreen(view) ||
		   widget_host_view->InitAsPopup(view, initial_rect);
		f: RenderWidgetHostImpl* render_widget_host_impl = 
								 RenderWidgetHostImpl::From(widget_host_view->GetRenderWidgetHost());
		   render_widget_host_impl->init();
	
	f：WebContentsImpl::CreateNewWidget
	m: pending_widget_views_
	m: created_widgets_
```

##destroy [关闭过程]：
third_party/WebKit/Source/core/html/HTMLSelectElement.cpp
```
HTMLSelectElement::menuListDefaultEventHandler(Event* event)
		f: hidePopup();
			m_popup->hide();  // m_popup PopupMenu对象
```
third_party/WebKit/Source/web/PopupMenuImpl.cpp
```
PopupMenuImpl::hide()
		m_chromeClient->closePagePopup(m_popup);
```

third_party/WebKit/Source/web/ChromeClientImpl.cpp
```
void ChromeClientImpl::closePagePopup(PagePopup* popup)
		m_webView->closePagePopup(popup);
```
third_party/WebKit/Source/web/WebViewImpl.cpp
```
WebViewImpl::closePagePopup(PagePopup* popup)
		m_pagePopup->closePopup();
```
third_party/WebKit/Source/web/WebPagePopupImpl.cpp
```
WebPagePopupImpl::closePopup()
		m_widgetClient->closeWidgetSoon();   //m_widgetClient ---> webwidgetclient ----> RenderWidget
```
sraf_porting/content/renderer/render_widget.cc
```
RenderWidget::closeWidgetSoon() 
		base::MessageLoop::current()->PostNonNestableTask(FROM_HERE, base::Bind(&RenderWidget::DoDeferredClose, this));
	DoDeferredClose
		Send(new ViewHostMsg_Close(routing_id_));
```
./sraf_porting/content/browser/renderer_host/render_widget_host_impl.cc
```
IPC_MESSAGE_HANDLER(ViewHostMsg_Close, OnClose)
	RenderWidgetHostImpl::OnClose()
		Shutdown();
	RenderWidgetHostImpl::Shutdown()
		Destroy()
	RenderWidgetHostImpl::Destroy()
		view_->Destroy();    // RenderWidgetHostViewBase view_;  public RenderWidgetHostView,
		delete this;
```
content/browser/renderer_host/render_widget_host_view_aura.h	
```
RenderWidgetHostViewAura ： RenderWidgetHostViewBase
	RenderWidgetHostViewAura::Destroy()
		delete window_;
```

##event [事件传递与分发]： 
sraf_porting/content/browser/renderer_host/render_widget_host_view_aura.cc
```
RenderWidgetHostViewAura::OnMouseEvent
		blink::WebMouseEvent mouse_event = MakeWebMouseEvent(event);
		host_->ForwardMouseEvent(mouse_event);
```
content/browser/renderer_host/render_widget_host_impl.cc
```
RenderWidgetHostImpl::ForwardMouseEvent(const WebMouseEvent& mouse_event)
		RenderWidgetHostImpl::ForwardMouseEventWithLatencyInfo
```



