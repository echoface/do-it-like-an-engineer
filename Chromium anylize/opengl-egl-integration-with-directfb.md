# OpenGL/EGL integration with DirectFB

分享一下我看到的几篇背景只是和结构性的内容;我们具体的实现就可以参考这个ozone的架构去对接eglgetdisplay， elgcreatePixMapsuface, eglCreateWindowSurface, elgSwapBuffers去做；在看这个之前，如果对chormium的Ozone整个架构设计不太了解的话，建议去看一下chromium design docments中的Ozone那一章；

先来看看在chromium GPU进程中我们的一个调用时序Ozone的实现：
![timing](/meet_chromium/img/EGL Init In Chromium.png)

下面这张是一张比较接近目前结构的一个概括图， 具体的更多内容可以参看chromium的design document页面；这个图来自[这个PPT内容](https://docs.google.com/presentation/d/1ou3qdnFhKdjR6gKZgDwx3YHDwVUF7y8eoqM3rhErMMQ/edit#slide=id.g17a920a23a_0_452)

![gpu output structure](/meet_chromium/img/chromium_gpu_design_structure.png)

第二个需要参考的就是chromium的Ozone实现，借助于Ozone我们才得以脱离目前市面上的各种各样的左面环境的依赖；可以让我们比较容易的对接到我目前项目中使用的“裸Linux”｛ps： embedded Linux Platform｝
[Chromium Ozone OVerview](/meet_chromium/reference/ozone_overview.md "Chromium Ozone OverView")
一个典型的例子是在WayLand上的实现参考， [https://github.com/01org/ozone-wayland](https://github.com/01org/ozone-wayland)； 完全看代码可能很难理解， 特别是现在大家都对wayland还不是很熟悉， 所以最好参考一下他们的设计说明一块看[Ozone-Wayland Architecture](https://docs.google.com/document/d/118Cmq_dedHOr4jfyVeE4jBhV7hXzhnaVCqegNMGano0/edit)

最后一个就是我们的具体实现， 因为我门的嵌入式linux平台上没有跑显示服务器，直接使用directfb进行的framebuffer的输出， 所以这部分需要一个directfb的binding；下面这个ppt可以让我们将directfb 的 surface、window 与 egl的surface 等对接起来；

![application structure](./img/dfb-egl_bindings.png)

![dfb api equals things](./img/directfb_elg_binding.png)


完整的PPT可以[参考这里](http://directfb.net/docs/DirectFB_EGL_2013-10-07.pdf)
