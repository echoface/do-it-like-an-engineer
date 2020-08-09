# How To Deep in Blink

这里引用一个知乎上的回答， 虽然这些链接大部分我都看过了， 但是仍旧觉得不够深入， 但是足够让自己更加全面的了解这些东西了：

看到回答里, 多数都没有回答到点子上, 还有些给了非常主观的意见而没有给出实际结论和分析过程.

题主的问题有四个: 

**1. Github 如何基于 Node.js 和 Chromium 开发 Atom?**

Atom 是基于 Atom-Shell ([atom/atom-shell · GitHub__](https://link.zhihu.com/?target=https%3A//github.com/atom/atom-shell)) 开发的, atom-shell 是一个将 Chromium 和 Node.js (在最近的版本中已经替换成了 io.js 了) 整合在一起的 shell 框架. 那么他是如何整合 node.js 和 chromium 的呢? Atom-Shell 在浏览器的底层和渲染层分别加入了 node.js 的事件循环, 由此在浏览器内核中驱动了 node.js. 之所以将渲染层和内核层的事件循环区分, 是为了 CEF3 的渲染架构而这么设计的, 而为了能够让渲染层之间, 以及渲染层和内核层之间通讯, 采用 ipc 进行封装, 具体的 ipc 实现我没深入去查看源代码, 应该是直接走了 Chromium 的 IPC 接口.   
类似的 Shell 技术还有 nw.js 和 bracket-shell. 但是这些 shell 技术都有差异, 具体的差异可以阅读这几篇文档:

[atom-shell/atom-shell-vs-node-webkit.md at master · atom/atom-shell · GitHub__](https://link.zhihu.com/?target=https%3A//github.com/atom/atom-shell/blob/master/docs/development/atom-shell-vs-node-webkit.md)  
[https://speakerdeck.com/zcbenz/practice-on-embedding-node-dot-js-into-atom-editor__](https://link.zhihu.com/?target=https%3A//speakerdeck.com/zcbenz/practice-on-embedding-node-dot-js-into-atom-editor)  
[https://speakerdeck.com/zcbenz/node-webkit-app-runtime-based-on-chromium-and-node-dot-js__](https://link.zhihu.com/?target=https%3A//speakerdeck.com/zcbenz/node-webkit-app-runtime-based-on-chromium-and-node-dot-js)

Github 的 Atom 就是在 Atom-Shell 的基础上, 通过 coffee-script 写页面端的表现, 通过 node.js/io.js 的整合处理 io 层的需求. 然后通过 atom-shell 整合操作系统中一些 native 窗口的能力.

**2. 有过来人能分享学习经验?**

学习经验倒也谈不上, 我基本上是阅读了一遍 atom-shell 官方的文档, 重点学习了一下如何使用 ipc 进行窗口间, 内核层之间的通讯方式以及页面编程相关的知识. 这个过程中, 我觉得有几个地方可以系统学习:

1. 通讯模型的建立:

为了更好的进行 ipc 通讯, 我们需要一些有效的经验模型来总结通讯的方法, 为此, 我找了两个通讯模型的文档进行学习:

[Getting Started with 'nanomsg'__](https://link.zhihu.com/?target=http%3A//tim.dysinger.net/posts/2013-09-16-getting-started-with-nanomsg.html)  
[http://zguide.zeromq.org/page:all__](https://link.zhihu.com/?target=http%3A//zguide.zeromq.org/page%3Aall)

通过对 nanomsg, zero-mq 中提出的几种通讯方式的总结, 我们渐渐地设计出符合我们需求的消息通讯编码规范, 和通讯类型. 

2. CSS 排版, DOM 页面渲染知识:

为了能够让我写的 GUI 高效的在页面中运转, 我需要掌握更多的关于浏览器如何渲染 DOM, 如何解析 CSS 等浏览器渲染内核的知识, 为此我阅读了以下文档:

[How Browsers Work: Behind the scenes of modern web browsers__](https://link.zhihu.com/?target=http%3A//www.html5rocks.com/en/tutorials/internals/howbrowserswork/) (这是一篇基础入门的好文章, 他让我在短短1个礼拜内, 通过自己的编码实践和扩展阅读理解了浏览器的大概的工作原理)  
[Getting Started With the WebKit Layout Code__](https://link.zhihu.com/?target=http%3A//blogs.adobe.com/webplatform/2013/01/21/getting-started-with-the-webkit-layout-code/) (这也是一篇非常好的文章, 他通过解析 Webkit 的底层 layout 代码, 让你明白整个浏览器是如何进行 css 排版工作的)  
[A Visual Method for Understanding WebKit Layout__](https://link.zhihu.com/?target=http%3A//blogs.adobe.com/webplatform/2013/02/05/a-visual-method-for-understanding-webkit-layout/) (这篇文章继承上一篇, 通过实践进一步理解 layout 的技术内容)  
[Rendering: repaint, reflow/relayout, restyle / Stoyan's phpied.com__](https://link.zhihu.com/?target=http%3A//www.phpied.com/rendering-repaint-reflowrelayout-restyle/) (这篇文章也是讲关于 reflow 的底层细节)  
[Understanding the CSS Specifications__](https://link.zhihu.com/?target=http%3A//www.w3.org/Style/CSS/read) (然后因为 css 的文档本身太晦涩, 我一个初入门 web 前端编程的人一开始没能读懂, 所以我就先找到了这篇进行学习)  
[Cascading Style Sheets Level 2 Revision 1 (CSS 2.1) Specification__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/CSS2/) (在那之后, 我进行了一些实践, 差不多觉得可以掌握了, 就通读了一遍这篇文档, 并通过少量编码, 完成大部分 css2 的排版计算过程, 打通了我心中对于排版的诸多疑问)这之后, 我又扩展阅读了以下一些 css 草案:  

* [CSS Animations__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/css3-animations/) CSS3 Animation 草案
* [CSS Transitions__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/css3-transitions/) CSS3 Transition 草案，transition和animaiton貌似有很多重合点，有待深究
* [Web Animations 1.0__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/web-animations/) Web Animation 草案
* [CSS Flexible Box Layout Module Level 1__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/css3-flexbox/) CSS3 Flexbox 草案
* [CSS Grid Layout Module Level 1__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/css3-grid-layout/) CSS3 Grid Layout 草案
* [CSS Transforms Module Level 1__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/css-transforms-1/) CSS3 Transform 草案，Transform 和 position 还是有不同之处，两个属性并没有过度冗余
* [CSS Shapes Module Level 1__](https://link.zhihu.com/?target=http%3A//www.w3.org/TR/css-shapes-1/) CSS3 Float Shape 草案，图文混排方面，属于进阶需求  
然后通过上面的几轮实践, 我又回过头来学习了以下几篇关于排版的知识点:  

* [Introduction to Layout in Mozilla__](https://link.zhihu.com/?target=https%3A//developer.mozilla.org/en-US/docs/Introduction_to_Layout_in_Mozilla) 这是 Mozilla Gecko 引擎的 Layout 技术细节
* [David Baron's CSS Playground__](https://link.zhihu.com/?target=http%3A//dbaron.org/css/) Mozilla 的开发者的Blog，里头有非常多技术详解
* [David's Inline Box Model__](https://link.zhihu.com/?target=http%3A//dbaron.org/css/2000/01/dibm) 这是上述开发者里的一片关于 Inline Box 的详解
* [The WebKit Open Source Project__](https://link.zhihu.com/?target=http%3A//www.webkit.org/coding/technical-articles.html) 这是 WebKit 中关于其技术细节的相关文档。
* [CSS animations and transitions performance: looking inside the browser__](https://link.zhihu.com/?target=http%3A//blogs.adobe.com/webplatform/2014/03/18/css-animations-and-transitions-performance/)

大概前前后后花了约 4 个月时间, 完成了整个 web 渲染和排版的基础知识. 

3. Node.js/io.js 学习

Node.js 的学习我是在项目中持续进行的, 这期间由于项目进度比较紧张, 我并没有很好的做好各种学习笔记, 所以不好意思, 没有特别多可以分享的经验. 

**3. 还有通过这种方式开发移动应用呢?**  

有一些 Hybrid 的应用通过相似的方法构建, 比较出名的有:

* [PhoneGap | Home__](https://link.zhihu.com/?target=http%3A//phonegap.com/)  
* [The Crosswalk Project__](https://link.zhihu.com/?target=https%3A//crosswalk-project.org/)  

这方面我接触的不多, 所以没有太多的经验可以分享.

**4. 基于 Node 开发类桌面应用有什么建议?**  
我觉得还是要从项目本身的需求出发点考虑, 如果你是一个 javascript 依赖较多的项目, 或者一个偏页面应用的项目, 那么基于 Node/Chromium 构建的桌面 APP 将给你带来非常好的基础结构, 让你专注在开发本身.