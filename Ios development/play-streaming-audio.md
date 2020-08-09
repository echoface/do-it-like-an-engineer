# 播放音频流媒体文件

在原来的教程中, 使用的是 MPMoviePlayerController 来播放音频文件; 在最新的系统上尝试那些代码的时候却给出了NS\_DEPRECATED\_IOS\(2\_0, 9\_0, "Use AVPlayerViewController in AVKit."\) 提示, 也就是说,这个代码从ios9开始就被废弃了. 提示说用AVkt框架中得AVPlayerViewController 来替代, 通过文档, 发现它集成子UIViewController, 而我并不打算呈现一个默认的UI界面. 而通过AVPlayerViewController中得成员, 可以看出它的内部是通过AVPlayer来实现的; 这样就很自然而然的找到了解决办法,

从代码的相关声明中可以明显的搞定如何使用, 下面看一个最简单的实例:

仅仅播放一个流媒体:

```js
var audioplayer: AVPlayer! = nil
audioplayer = AVPlayer();
audioplayer.replaceCurrentItemWithPlayerItem(AVPlayerItem(URL: NSURL(string: "http://x.com/xxxx/xxx.mp3")!))
audioplayer.play(); 
```

这里我使用了空参数的构造函数, 事实上, AVPlayer还提供了另外的两个构造函数,

* public init\(URL: NSURL\)

* public init\(playerItem item: AVPlayerItem\)


他们分别从一个URL 和 一个AVPlayerItem 来构造一个对象, 而对于AVPlayer来说, 没一个播放的对象都是一个AVPlayerItem, 正如我上面的代码中得函数 **replaceCurrentItemWithPlayerItem** , 我们可以在播放的任何时刻, 通过这个函数来切换播放; AVPlayerItem 还通过一系列的扩展,帮助完成了一些列的功能, 我们最关注的几个: 播放,暂停, 前进,后退, 播放速率, 这些在AVPlayer类中都有完整函数定义来满足我们的需求;

改变进度的几个函数:

```js
public func seekToTime(time: CMTime)
public func seekToTime\(time: CMTime, completionHandler: (Bool) -&gt; Void)
public func seekToTime\(time: CMTime, toleranceBefore: CMTime, toleranceAfter: CMTime)
public func seekToTime\(time: CMTime, toleranceBefore: CMTime, toleranceAfter: CMTime, completionHandler: (Bool) &gt; Void)
//还有 seekToDate 系列的函数同样可以达到同样地目的
public func seekToDate(date: NSDate)
....
```

```
 public func pause()
 public func play()
```

另外, 我们可以通过添加侦听, 来获取到时间的变化和歌曲长度的变化, 比如说你要在播放时间变化时update 你用来显示播放进度的 **progressbar** ; 当然在一个**viewcontroller **disappear的时候通过 **removeTimeObserver**来移除侦听是个不错的选择;

```js
 public func addPeriodicTimeObserverForInterval(interval: CMTime, queue: dispatch_queue_t?, usingBlock block: (CMTime) -> Void) -> AnyObject 
 public func addBoundaryTimeObserverForTimes(times: [NSValue], queue: dispatch_queue_t?, usingBlock block: () -> Void) -> AnyObject
 public func removeTimeObserver(observer: AnyObject) 
```

### 如果我们需要播放一个歌曲列表怎么办?

---

一个AVplayer的派生类 **AVQueuePlayer** 已经为我们准备好了这样的功能, 这样就省去了自己上一首下一首等等的事情了, 既然是派生类, 所以AVPlayer有的他都有, 另外它实现了几个对于这种列表播放需要的功能

它可以用一个**AVPlayerItem**的数组来初始化这个**AVQueuePlayer**

```js
public init(items: [AVPlayerItem]) // 使用一个数组来初始化播放列表
public func items() -&gt; [AVPlayerItem] // 取得这个列表
public func advanceToNextItem() //下一首 
public func insertItem(item: AVPlayerItem, afterItem: AVPlayerItem?) // 在列表中插入一个播放对象, 不过插入前最好判断一下能否插入播放对象, 具体看类的函数 canInsertItem->Bool
//还有下面的这个: 是否自动播放下一首....
public enum AVPlayerActionAtItemEnd : Int { 
 case Advance
 case Pause
 case None
}
```

