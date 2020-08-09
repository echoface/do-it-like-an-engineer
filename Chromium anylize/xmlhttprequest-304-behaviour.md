# XMLHttpRequest 304 Behaviour Specification

[http://stackoverflow.com/questions/13783442/how-to-tell-if-an-xmlhttprequest-hit-the-browser-cache](http://stackoverflow.com/questions/13783442/how-to-tell-if-an-xmlhttprequest-hit-the-browser-cache "XMLHttpRequest 304 behaviour")

[https://www.w3.org/TR/2006/WD-XMLHttpRequest-20060927/](https://www.w3.org/TR/2006/WD-XMLHttpRequest-20060927/ "XMLHttpRequest specification ")

> For 304 Not Modified responses that are a result of a user agent generated conditional request the user agent must act as if the server gave a 200 OK response with the appropriate content. The user agent must allow author request headers to override automatic cache validation \(e.g. If-None-Match or If-Modified-Since\), in which case 304 Not Modified responses must be passed through. \[HTTP\]

---

按照specification的要求， 当页面发起一个XMLHttpRequest请求的时候， 如果服务器返回304（Not Modified）浏览器应该像处理状态200一样， 并且返回正确的内容， 同时浏览器必须需要支持允许用户去修改http的请求头（通过if-none-match， if-Modified-since）来控制是否使用cache的内容， 在加了请求头内容的时候， 返回的响应就因该是304， 而不是200；

