# http xml request IOS9 网络请求

在ios 7 以前, 发起http 气球还是通过**NSURLRequest **来发起同步或一部的请求, 传入一个闭包来出来返回的数据或者错误, 比如下面这段代码这样;

```js
 func onSearch(url:String) { 
   let nsUrl: NSURL = NSURL(string: url)!
   let request: NSURLRequest = NSURLRequest(URL: nsUrl)

   NSURLConnection.sendAsynchronousRequest(request, queue: NSOperationQueue.mainQueue(), completionHandler: {
 (response:NSURLResponse?, data: NSData?, error:NSError?)->Void in

   let jsonData = try! NSJSONSerialization.JSONObjectWithData(data!, options: NSJSONReadingOptions.MutableContainers) as! NSDictionary

   //var jsonData:NSDictionary = NSJSONSerialization.JSONObjectWithData(data, options:NSJSONReadingOptions.MutableContainers) as! NSDictionary
   //self.delegate?.didRecieveResults(jsonData)
   })
 }
```

而新的系统中, apple 官方明确地推荐使用Session 回话 和 task 的形式来创建人物和完成请求了,通过 **NSURLSession** 来创建一个URL会话, 使用一系列内置的函数可以将任务包装成 Task 的形式, 之后通过Task的Resume函数来启动一个URL会话任务, 看下面的代码:

```javascript
 let nsUrl: NSURL = NSURL(string: url)! 
 let request: NSURLRequest = NSURLRequest(URL: nsUrl)

 let urlSession = NSURLSession.sharedSession()
 let datatask = urlSession.dataTaskWithRequest(request, completionHandler: {
   (data: NSData?, response: NSURLResponse?, error:NSError?)->Void in

   if (error != nil) {
     print("url request load data error", error?.description)
     return
   } else if data != nil {
     let jsonData = try? NSJSONSerialization.JSONObjectWithData(data!, options:NSJSONReadingOptions.MutableContainers)
     self.delegate?.didRecieveResults(jsonData as! NSDictionary)
   }
 })
 datatask.resume()
```

