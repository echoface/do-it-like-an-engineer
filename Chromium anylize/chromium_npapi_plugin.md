#Plugin


现在chromium浏览器中有NPAPI 和 新的PPAPI 插件， 两种插件区分是通过GetInfoForPlugin（）函数获得一个plugin_info的对来来判断是创建PPAPI 还是 NPAPI 插件， 这里我们要区分看在chromium中的扩展 和 插件的区别， 我们这里说明的是插件plugin，而非扩展extension


创建分为两个大的步骤， 创建整个关系链 + 插件instance的Init

###plugin 的创建


第一个过程： 创建并初始化Plugin Instance
---
> 下面是一个大字的callstack， 在大概40版本开始， NPAPI就渐渐的被移除了，到现在version 51， 最新的code里面基本上已经看不到NPAPI的痕迹了， 就连blink面也都完全被移除干净了...所以，接下来chromium已经完全是PPAPI的天下了， 不过对于我现在的工作而言， 真的是让人吐血的暴击呀。一千点，不！ 一万点

```cpp  
core/html/HTMLPlugInElement.cpp:599: 
    call: widget = frame->loader().client()->createPlugin(this, url, paramNames, paramValues, mimeType, loadManually, policy);

third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp
  call: WebPlugin* webPlugin = m_webFrame->client()->createPlugin(m_webFrame, params);
  call: **if (!webPlugin->initialize(container.get()))**    (#第二条线，创建后plugin的初始化)

content/renderer/render_frame_impl.cc ： 继承blink里面的WebFrameClient.h
blink::WebPlugin* RenderFrameImpl::createPlugin
  call: CreatePlugin(frame, info, params_to_use);

content/renderer/npapi/webplugin_impl.cc
blink::WebPlugin* RenderFrameImpl::CreatePlugin
    call: return new WebPluginImpl(frame, params, info.path, render_view_, this);
```

在创建NPAPI的这个webpluginImpl类的构造函数中， 仅仅是将params存起来而已，真的是啥都没干，不行你看
```cpp
WebPluginImpl::WebPluginImpl(
    WebFrame* webframe,
    const WebPluginParams& params,
    const base::FilePath& file_path,
    const base::WeakPtr<RenderViewImpl>& render_view,
    RenderFrameImpl* render_frame)
    : windowless_(false),
      window_(gfx::kNullPluginWindow),
      accepts_input_events_(false),
      render_frame_(render_frame),
      render_view_(render_view),
      webframe_(webframe),
      delegate_(NULL),
      container_(NULL),
      npp_(NULL),
      plugin_url_(params.url),
      load_manually_(params.loadManually),
      first_geometry_update_(true),
      ignore_response_error_(false),
      file_path_(file_path),
      mime_type_(base::UTF16ToASCII(params.mimeType)),
      loader_client_(this),
      weak_factory_(this) {
  DCHECK_EQ(params.attributeNames.size(), params.attributeValues.size());
  base::StringToLowerASCII(&mime_type_);

  for (size_t i = 0; i < params.attributeNames.size(); ++i) {
    arg_names_.push_back(params.attributeNames[i].utf8());
    arg_values_.push_back(params.attributeValues[i].utf8());
  }

  // Set subresource URL for crash reporting.
  base::debug::SetCrashKeyValue("subresource_url", plugin_url_.spec());
}
```


第二个过程： 创建plugin整个类的关系链
---
至此， 我们整个render进程中， plugin 从一个html的element一步步的创建出一系列相关类的对象， 因为创建可能失败， 所以我们需要确保创建成功， 一旦创建成功， 我们就可以开始初始化我们真正的plugininstance， 在这个第二过程中， 会完成plugin进程中相应的object的创建；
从我们上面的分析中『看下面的代码』， 可以看出我们创建好webplugin对象成功之后， 在FrameLoaderClientImpl.cpp的createplugin函数中， 调用了webPlugin的Initialize函数， 并将创建好的一个Container传递了进去， 这个类**WebPluginContainerImpl**的Container对象会OWnership这个当前创建的plugin的生命周期；

    third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp
      call: WebPlugin* webPlugin = m_webFrame->client()->createPlugin(m_webFrame, params);
      call: **if (!webPlugin->initialize(container.get()))**    (#第二条线，创建后plugin的初始化)

下面的内容就是webplugin的初始化过程， 里面首先做了个判断， 确保这个plugin的render_view\_ 是存在的，之后这里构造了一个WebPluginDelegateProxy对象并通过Initialize函数初始化；初始化中完成了下面几件事情
- 1. 发送一个FrameHostMsg_OpenChannelToPlugin IPC来初始化Plugin的IPC channel；
- 2. 发送一个PluginMsg_CreateInstance IPC给Plugin进程创建PluginInstance
- 3. 确定2完成后， 发送一个PluginMsg_Init IPC消息给Plugin初始化这个PluginInstance；
- 4. 通过render_view\_->RegisterPluginDelegate(this); 将自己注册给RenderViewImpl

到这个函数完成， 整个plugin Instance 就完整的起来了。这里发送的IPC 全部是同步的IPC消息， 上面其实每一个IPC的接收端都有一段长长的故事；

#### focus 2： PluginMsg_CreateInstance
在接收到PluginMsg_CreateInstance消息后， 调用OnCreateInstance函数创建了一个WebPluginDelegateStub的对象，并存到一个plugin_stubs\_数组中； 因为一个页面上可能会使用多个plugin的对象；
content/plugin/plugin_channel.cc:266:    IPC_MESSAGE_HANDLER(PluginMsg_CreateInstance, OnCreateInstance)
```cpp
void PluginChannel::OnCreateInstance(const std::string& mime_type,
                                       int* instance_id) {
  *instance_id = GenerateRouteID();
  scoped_refptr<WebPluginDelegateStub> stub(new WebPluginDelegateStub(mime_type,
                                                                         *instance_id, this));
  AddRoute(*instance_id, stub.get(), NULL);
  plugin_stubs_.push_back(stub);
}
```
#### focus 3： 
在第二点中创建好WebPluginDelegateStub之后， 发送一个Init的消息给到pluginDelegateStub，响应函数如下：这里我删除了大部分无关的代码， 只保留了主要流程的内容：大致完成了如下部分的工作
- 创建一个WebPluginProxy对象，//仅仅创建了对象
- 创建了WebPluginDelegateImpl 对象// 通过static方法创建 PluginLib对象并初始化 + 创建PluginInstance
- 设置delegate关系和注册NPObject的owner
- 初始化webplugindelegate对象；// 完成一些Plugin相关的平台初始化... 
```CPP
void WebPluginDelegateStub::OnInit(const PluginMsg_Init_Params& params,
                                   bool* transparent,
                                   bool* result) {
... ...
webplugin_ = new WebPluginProxy(channel_.get(),
                                  instance_id_,
                                  page_url_,
                                  params.host_render_view_routing_id);
  delegate_ = WebPluginDelegateImpl::Create(webplugin_, path, mime_type_);
  ... ...
  webplugin_->set_delegate(delegate_);
  WebBindings::registerObjectOwner(delegate_->GetPluginNPP());
  *result = delegate_->Initialize(params.url,
                                    arg_names,
                                    arg_values,
                                    params.load_manually);
  ... ...
}
```

在静态方法WebPluginDelegateImpl::Create(webplugin_, path, mime_type_);的调用中调用如下方法
- scoped_refptr<PluginLib> plugin_lib(PluginLib::CreatePluginLib(filename));
- NPError err = plugin_lib->NP_Initialize();
- scoped_refptr<PluginInstance> instance(plugin_lib->CreateInstance(mime_type));
- return new WebPluginDelegateImpl(plugin, instance.get());

```cpp
PluginLib* PluginLib::CreatePluginLib(const base::FilePath& filename) {
  ... ...
  WebPluginInfo info;
  if (!PluginList::Singleton()->ReadPluginInfo(filename, &info))
    return NULL;

  return new PluginLib(info);
}
```
上面的CreatePluginLib函数中， 里面通过读取到pluin相关的信息， 通过这个信息构造了一个PluginLib对象并返回；并通过获取到的信息创建了PluginLib对象； 之后通过**NP_Initialize**函数初始化了PluginLib； 初始化的过程中， 通过PluginEntryPoints结构体保存的entry pointer会具体初始化我们自己编写的plugin的具体内容；

在WebPluginDelegateImpl::create这个静态函数中紧接着调用了plugin_lib->createInstance(),函数, createInstanceh函数中， 创建并返回了PluginInstance对象； 这个instance会传递给WebPluginDelegateImpl对象， 这里用的是Scoped_refptr，他相对于scoped_ptr增加了应用计数功能， 所以最终instance的生命周期在WebPluginDelegateImpl中完成；

在回到 ×focus 3× 那里， 创建完WebPluginDelegateImpl对象后，将WebPluginDelegateImpl对象设置成webplugin的delegate对象， 并调用delegate_->Initialize初始化了WebPluginDelegateImpl对象；

---
到这里为止， 整个plugin instance的创建完成了， 在FrameLoaderClientImpl对象中得到创建好的webplugin对象；




content/renderer/npapi/webplugin_impl.cc
```CPP
bool WebPluginImpl::initialize(WebPluginContainer* container) {
  if (!render_view_.get()) {
    LOG(ERROR) << "No RenderView";
    return false;
  }

  /*!!!
    这里很重要，在init的过程中， 构造了一个WebPluginDelegateProxy， 并将
    render_view_ 传递给了WebPluginDelegateProxy，而在webplugindelegateproxy
    的构造函数中通过 **render_view_->RegisterPluginDelegate(this);**向
    render_view_中传注册了这个delegate， 而这个delegate负责处理 PluginHostMsg**
    一些列来自于pluginhost的消息，delegate中一方面可以访问webpluginimpl去访问
    Plugin，一方面可以和render_view_, render_frame_进行交互；
  */
  WebPluginDelegateProxy* plugin_delegate = new WebPluginDelegateProxy(
      this, mime_type_, render_view_, render_frame_);

  // Store the plugin's unique identifier, used by the container to track its
  // script objects.
  npp_ = plugin_delegate->GetPluginNPP();

  // Set the container before Initialize because the plugin may
  // synchronously call NPN_GetValue to get its container, or make calls
  // passing script objects that need to be tracked, during initialization.
  SetContainer(container);

  bool ok = plugin_delegate->Initialize(
      plugin_url_, arg_names_, arg_values_, load_manually_);
  if (!ok) {
    plugin_delegate->PluginDestroyed();

    blink::WebPlugin* replacement_plugin =
        GetContentClient()->renderer()->CreatePluginReplacement(
            render_frame_, file_path_);
    if (!replacement_plugin)
      return false;

    // Disable scripting by this plugin before replacing it with the new
    // one. This plugin also needs destroying, so use destroy(), which will
    // implicitly disable scripting while un-setting the container.
    destroy();

    // Inform the container of the replacement plugin, then initialize it.
    container->setPlugin(replacement_plugin);
    return replacement_plugin->initialize(container);
  }

  delegate_ = plugin_delegate;

  return true;
}
```

可以看到在webpluginimpl中创建并管理了一个WebPluginDelegateProxy\* plugin_delegate 对象, 并调用了它的Initialize函数，来初始化WebPluginDelegateProxy； 这里很重要， 这个proxy类搭建起了plugin进程和render进程的桥梁，










析构， destroy plugin instance
---

在third_party/WebKit/Source/web/FrameLoaderClientImpl.cpp 创建的webplugin会被
third_party/WebKit/Source/web/WebPluginContainerImpl.cpp 中的webpluginContainer管理和维护着， 并在它的析构函数中，调用m_webPlugin->destroy(); 来析构整个plugin 一些列的过程


- content/renderer/npapi/webplugin_impl.cc

NPObject* WebPluginImpl::scriptableObject()
  call: SetContainer(NULL);
void WebPluginImpl::SetContainer(WebPluginContainer* container)
  call: TearDownPluginInstance(NULL);
void WebPluginImpl::TearDownPluginInstance(WebURLLoader* loader_to_ignore)
  call: delegate_->PluginDestroyed(); //这里的delegate_ 是WebPluginDelegateProxy 对象

- content/renderer/npapi/webplugin_delegate_proxy.cc

void WebPluginDelegateProxy::PluginDestroyed()
  call: render_view_->UnregisterPluginDelegate(this);
  call: Send(new PluginMsg_DestroyInstance(instance_id_));
 
- content/plugin/plugin_channel.cc

IPC_MESSAGE_HANDLER_DELAY_REPLY(PluginMsg_DestroyInstance, OnDestroyInstance)
void PluginChannel::OnDestroyInstance(int instance_id,IPC::Message* reply_msg)
  call: plugin_stubs_.erase(plugin_stubs_.begin() + i); //智能指针vector 调用stub析构

- content/plugin/webplugin_delegate_stub.cc

WebPluginDelegateStub::~WebPluginDelegateStub()
  call: DestroyWebPluginAndDelegate(plugin_scriptable_object_, delegate_, webplugin_);

static void DestroyWebPluginAndDelegate(base::WeakPtr<NPObjectStub> scriptable_object...)
  pos1: call: delegate->PluginDestroyed(); // WebPlugin must outlive WebPluginDelegate.
  pos2: call：WebBindings::unregisterObjectOwner(owner);
  pos3: call: delete webplugin;



##pos 1
- content/child/npapi/webplugin_delegate_impl.cc

void WebPluginDelegateImpl::PluginDestroyed()
  call: delete this;

- content/child/npapi/webplugin_delegate_impl_aura.cc

WebPluginDelegateImpl::~WebPluginDelegateImpl()
  call: DestroyInstance();
 
- content/child/npapi/webplugin_delegate_impl.cc

void WebPluginDelegateImpl::DestroyInstance()
  instance_->NPP_Destroy();
  
- content/child/npapi/plugin_instance.cc
  call: npp_functions_->destroy(npp_, &savedData);
  
##pos 3:

- content/plugin/webplugin_proxy.cc

WebPluginProxy::~WebPluginProxy()
  call: 如果有pluginelement【type： NPObject】： WebBindings::releaseObject(plugin_element_);
  call: 如果有window_object【type： NPObject】： WebBindings::releaseObject(window_npobject_);