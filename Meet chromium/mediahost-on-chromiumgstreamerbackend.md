# 三星ChromiumGStreamerBackend中的MediaHost 与 MediaProcess


通过`MediaProcessHost::Get`接口可以得到`MediaProcessHost`对象， 这样便可以在UI线程当中发送ipc消息给多媒体进程；