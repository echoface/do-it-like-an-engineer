# DOM TREE 的创建分析

工作中， 陆陆续续的分散的将Chromium的各个部分都看了些， 虽然content中的居多， 但是Blink中的也有接触，但是不够深入， 也不够全面； 所以希望在此文的背景之下， 整理这些知识和内容， 在自己的脑子里形成一个全面的MindMap来理解和继续接下来的工作中的内容； 学无止境，也不一定理解的全部正确；如果有人看到，见谅；｛肯定有理解不多的...｝

开始之前，我先贴上来一段数据的获取的callstack， 这里就不解释为什么webkit中会收到这份数据了；这个callstack灰很好的明了的解释这段数据是怎么从Browser端传递过来的；下面是ResourceLoader中收到数据的函数didRecieveData之前的整个调用：


简单来说就是， 当发起的一个url_request的时候，会在Browser端创建一个RULRequestJob类对象去取数据， 取的过程中有可能是在appcache、httpcache等等不同的来源， 当它们通过一个StartAsync发起异步请求之后会受到来自数据可读的通知， 之后在数据可读的时候读取数据之后通过task的形式通知到url_request_job当中， 通过`NotifyReadCompleted`将消息传递给UrlRequest， UrlRequest发起响应将消息给到ResourceLoader， 之后ResourceLoader通过`StartReading`函数开始读取数据；读取完成之后调用OnReadCompleted,之后便在CompleteRead函数调用handler的处理函数`OnReadCompleted`中， 而这个handler又根据资源加载的方式分为异步加载的handler和detachable、download等等之类的， 我们最常见的淡然就是异步加载；在函数中通过sharememory的方式保存起来， 之后通过IPC `ResourceMsg_DataReceived`通知给Render进程；

```shell
#0  content::AsyncResourceHandler::OnReadCompleted (this=0x1b91baaec860, bytes_read=1260, defer=0x7fffd1dd6f7f)
    at ../../content/browser/loader/async_resource_handler.cc:419
#1  0x00007ffff4a9ba9c in content::InterceptingResourceHandler::OnReadCompleted (this=0x1b91ba48d7a0, bytes_read=1260, defer=0x7fffd1dd6f7f)
    at ../../content/browser/loader/intercepting_resource_handler.cc:89
#2  0x00007ffff4a9db7b in content::LayeredResourceHandler::OnReadCompleted (this=0x1b91ba265260, bytes_read=1260, defer=0x7fffd1dd6f7f)
    at ../../content/browser/loader/layered_resource_handler.cc:61
#3  0x00007ffff4a9f71e in content::MimeSniffingResourceHandler::OnReadCompleted (this=0x1b91bab20620, bytes_read=1260, defer=0x7fffd1dd6f7f)
    at ../../content/browser/loader/mime_sniffing_resource_handler.cc:198
#4  0x00007ffff4a9db7b in content::LayeredResourceHandler::OnReadCompleted (this=0x1b91ba25dd60, bytes_read=1260, defer=0x7fffd1dd6f7f)
    at ../../content/browser/loader/layered_resource_handler.cc:61
#5  0x00007ffff4b02950 in content::ResourceLoader::CompleteRead (this=0x1b91baaa21a0, bytes_read=1260)
    at ../../content/browser/loader/resource_loader.cc:638
#6  0x00007ffff4b02417 in content::ResourceLoader::OnReadCompleted (this=0x1b91baaa21a0, unused=0x1b91ba12a820, bytes_read=1260)
    at ../../content/browser/loader/resource_loader.cc:376
#7  0x00007ffff0a0ee9f in net::URLRequest::NotifyReadCompleted (this=0x1b91ba12a820, bytes_read=1260)
    at ../../net/url_request/url_request.cc:1161
#8  0x00007ffff0a3e6fa in net::URLRequestJob::SourceStreamReadComplete (this=0x1b91b9ebb420, synchronous=false, result=1260)
    at ../../net/url_request/url_request_job.cc:677
```

