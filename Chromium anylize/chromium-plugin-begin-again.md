# Chromium Plugin Begin Again

在begin again之前，先搞清楚两个概念** chrome extensions** & **web Plugin**

## chrome extensions

official infomation：[extensions](https://developer.chrome.com/extensions)

> Extensions are small software programs that can modify and enhance the functionality of the Chrome browser. You write them using web technologies such as HTML, JavaScript, and CSS.

也就是说， 扩展在chrome上通常是用htm、javascript、css编写的用来修改或者增强浏览器功能的一个应用；比如：一个字典扩展可以通过访问clip Board来里面复制的内容来翻译成不同的语言，让后通过一个小的浮动页面（类似气泡弹窗）来显示结果;

## Plugins

说道这个词， 大家可能最容易想到的可能就是flash插件，其实插件就是开发者遵循一定规范的应用程序接口编写出来的程序；而且这个程序是用来扩展页面功能用的；比如说我要支持一个新的音频格式xz，开发一个插件是用来支持“audio\/xz”这种content type的plugin、 那么当浏览器在解析html的时候遇到这种类型的内容时，发现默认的浏览器中无法正确的处理渲染这个标签，如果这时候有支持这种type的plugin，那么就会使用相应的插件来支持播放这种xz格式的音频流；
最早plugin是由浏览器的元祖Netscape定义的一个叫做** Netscape Plugin Application Programming Interface \(NPAPI\) **这样的一个接口规范，默默的被大多数后来的浏览器支持和使用， 但是随着现代化浏览器的发展，它已经显现出明显的不足了，所以各个Browser厂商各种又开发出自己的规范；MS的ActiveX， chrome的PPAPI都算是这个范畴了， 而今天的主角是Google Chrome在NPAPI的基础上演进出来的PPAPI

PPAPI在 Google Native Client \(NaCl\) 技术基础上开发出的一套规范， 他的目标简单来说就是想使得插件更加**统一** **安全** **强大** **易开发**；
完整的一个介绍看下面的这个:

1. Uniform semantics for NPAPI across browsers.
2. Execution in a separate process from the renderer-browser.
3. Standardize rendering using the browser's compositing process.
4. Defining standardized events, and 2D rasterizing functions.
5. Initial attempt to provide 3D graphics access.
6. Plugin registry.

google chrome 在我现在工作中的版本V39NPAPI和PPAPI都是支持的，但是从V42起，查阅的源码中NPAPI相关的代码逐渐的被一点点去除了， 到了现在的52， 整个Chrome中的源代码中， 几乎已经找不到相关的code了；

当一个页面主文档下载完毕，也就是当收到browser端塞过来的一段数据； 从didRecieveData到Parse这段数据；最后到PluginDocument中的CreateDocumentStructure开始，在创建整个Plugin Tag的过程中创建了整个Plugin Instance实例；

![NPAPI PLUGIN 流程图](/meet_chromium/img/Chromium_Plugin.png)
```c
现在我们的Plguin的创建有下面几点信息：

在HTMLObjectElement::parseAttribute 的时候调用
requestPluginCreationWithoutLayoutObjectIfPossible();
	-> createPluginWithoutLayoutObject
		-> loadPlugin 这条路中我们有做一些修改


在HTMLEmbedElement::parseAttribute 的时候调用
requestPluginCreationWithoutLayoutObjectIfPossible();
	-> createPluginWithoutLayoutObject
		-> loadPlugin 这条路中我们有做一些修改

上面那两种情况都是正常的parse和create的一个流程， 另外我们在LayoutTreeBuilderForElement对象中继承了LayoutTreeBuilder对象的createLayoutObjectIfNeeded()函数， 在这个函数中， 判断如果不需要创建LayerOutObject的的话就创建LayoutObject， 否则的话
	
		void LayoutTreeBuilderForElement::createLayoutObjectIfNeeded()	
		{
	    	if (shouldCreateLayoutObject()) {
	    	    createLayoutObject();
	    	} else if (isHTMLObjectElement(*m_node) || isHTMLEmbedElement(*m_node)) {
	        	toHTMLPlugInElement(m_node->requestPluginCreationWithoutLayoutObjectIfPossible();
			}
		}


DOMImplementation.cpp 中， 我们hack了createDocument函数， 当type == text/html时， 我们通过自己的一个函数DOMImplementation::createSrafDocument来根据不同的网页类型来创建XHTML 类型的document或者HTMLDocument




Plugin的destroy

ReinitializePluginForResponse
WebPluginImpl::TearDownPluginInstance
WebPluginDelegateProxy::PluginDestroyed
	||
	|| PluginMsg_DestroyInstance ipc to plugin 
	||
PluginChannel::OnDestroyInstance
	WebPluginDelegateStub::~WebPluginDelegateStub
		DestroyWebPluginAndDelegate In webplugin_delegate_stub.cc
			WebPluginDelegateImpl::~WebPluginDelegateImpl
				》 WebPluginDelegateImpl::DestroyInstance
					》 PluginInstance::NPP_Destroy
						》 npp_functions_->destroy ====> SrafHbbTVPlugin::NPP_Destroy
							》 HbbtvNppDataObject::deinitialize
```