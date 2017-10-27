# 遇见Chromium

update:  新篇章

在Blink内与Cotent架构上折腾两年了， 这两年收获很多，前前后后将content各个部分或多或少的都接触到了，Chromium的Design Documents也前前后后翻了几回了，这个web世界的基本内容加载， 解析、DOM结构构建、LayoutObject的构建、到最后依据Css2.1中所规范的Stacking Context而划分出的GraphicsLayer；disable-gpu情况下的softwareOutput也有涉及，但是不够深入, 现在日益复杂的compositing到GPU output需要我静下心来了解，在一些列代码的阅读中开始思考更加深入的问题；如果想走的更远，是时候进一步深入了；这很艰难，但是不得不走；
- 更加深入的了解Painting 和 compositing相关的内容，
- 深入GPU的世界，理解GPU的思维模式
- 基于模块的完整学习，而不再仅仅具体问题分析和实现；

update:
最近看GPU egl的整合， 因为是裸Linux平台， 用的是DIrectFB做的backstore， 有些非常有用的整理；**[See Here](/meet_chromium/opengl-egl-integration-with-directfb.md)**

---

加入seraphic 是2015年的事情事情， 距离我写下句话的时候整整1年时间。这期间有对技术的兴奋也有失落。同时我也在成长。

- [**How Browser Engine Work，这个作为入门应该算是比较全面也很准确，有很多基础性的设计的解释和说明**](https://www.html5rocks.com/zh/tutorials/internals/howbrowserswork/)

- [**chromium design document Chromium项目的设计文档，可能过时了， 但是有整体的参考意义**](https://www.chromium.org/developers/design-documents)

- [**PPT compositing in Blink, 在看具体代码前最好先把design document中的相关内容看一看**](https://docs.google.com/presentation/d/1dDE5u76ZBIKmsqkWi2apx3BqV8HOcNf4xxBdyNywZR8/edit#slide=id.gc4b85070_1723)

> 这个我在自己的google driver 存了一份，虽然和现在的code有天大的区别， 但是了解compositing 的整个思路以及如何合并paiter内容， 如何分层，stacking context的设计逻辑基本上和现有的差不了太多， 但是这个和现在正在开发和设计的sliming painting区别很大， 算作是参考吧， 不然就compositing这块的代码一句注释没有，还有那么多状态， 看起来很费劲; 有需要的 [https://docs.google.com/presentation/d/1DJkD-ExVehP8rxr0tMW1e5rIQHQ9eS4jcNDSlYlL0xk/edit?usp=sharing](https://docs.google.com/presentation/d/1DJkD-ExVehP8rxr0tMW1e5rIQHQ9eS4jcNDSlYlL0xk/edit?usp=sharing)

- 代码导读的话， 罗升阳的博客或者书， 解答的比较详细；篇幅也比较全；

- 对chromium进行除了浏览器本身功能扩展的话， 有两个比较好的例子， 一个是QtWebEngine（基于content api的开发）的实现和QtWebChannel（对内核的扩展）的实现｛ps： take it easy， 放心去读吧， 代码量很少， 但是一整套很完整，我自己就是读的这部分代码｝，另外一个就是atom-shell，现在的electron的实现； 

