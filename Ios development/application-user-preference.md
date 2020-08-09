# Application User Preference

IOS应用程序中, 在系统设置页面里面包含了每一个安装了的应用的配置选项, 程序中, 我们只需要将一些设置写入用户首选项的配置里, 这些信息就会和我们应用一直存在;

在Foundation基础框架中, 我们通过**NSUserDefaults** 对象来设置和访问我们的应用的首选项数据; **NSUserDefaults**类维护了一系列的方法用来访问和设置数据;下面是我从类中截取的一些方法

```swift
    /*!
     +standardUserDefaults returns a global instance of NSUserDefaults configured to search the current application's search list.
     */
    public class func standardUserDefaults() -> NSUserDefaults
    
    /// +resetStandardUserDefaults releases the standardUserDefaults and sets it to nil. A new standardUserDefaults will be created the next time it's accessed. The only visible effect this has is that all KVO observers of the previous standardUserDefaults will no longer be observing it.
    public class func resetStandardUserDefaults()

    /*!
     -objectForKey: will search the receiver's search list for a default with the key 'defaultName' and return it. If another process has changed defaults in the search list, NSUserDefaults will automatically update to the latest values. If the key in question has been marked as ubiquitous via a Defaults Configuration File, the latest value may not be immediately available, and the registered value will be returned instead.
     */
    public func objectForKey(defaultName: String) -> AnyObject?
    
    /*!
     -setObject:forKey: immediately stores a value (or removes the value if nil is passed as the value) for the provided key in the search list entry for the receiver's suite name in the current user and any host, then asynchronously stores the value persistently, where it is made available to other processes.
     */
    public func setObject(value: AnyObject?, forKey defaultName: String)
    
    /// -removeObjectForKey: is equivalent to -[... setObject:nil forKey:defaultName]
    public func removeObjectForKey(defaultName: String)
    
    public func integerForKey(defaultName: String) -> Int
    /// -floatForKey: is similar to -integerForKey:, except that it returns a float, and boolean values will not be converted.
    public func floatForKey(defaultName: String) -> Float
    /// -doubleForKey: is similar to -doubleForKey:, except that it returns a double, and boolean values will not be converted.
    public func doubleForKey(defaultName: String) -> Double

    public func setFloat(value: Float, forKey defaultName: String)
    /// -setDouble:forKey: is equivalent to -setObject:forKey: except that the value is converted from a double to an NSNumber.
    public func setDouble(value: Double, forKey defaultName: String)
    /// -setBool:forKey: is equivalent to -setObject:forKey: except that the value is converted from a BOOL to an NSNumber.
    public func setBool(value: Bool, forKey defaultName: String)
    /// -setURL:forKey is equivalent to -setObject:forKey: except that the value is archived to an NSData. Use -URLForKey: to retrieve values set this way.
    @available(iOS 4.0, *)
    public func setURL(url: NSURL?, forKey defaultName: String)
```

基本上可以看出, **NSUserDefaults** 类提供了一系列的setxxx forkey的方法和 xxxforkey的方法来设置和获取应用程序首选项的值; 同时还提供了静态的方法standardUserDefaults()来获取一个default的NSUserDefaults对象; 所以我们在程序中, 只需要在必要的时候通过这个default的对象去设置和读取我们的配置即可;

例如:
---

```swift
let keepalive: Bool!
override func viewDidLoad() {
  super.viewDidLoad()
    
  let userdefaults = NSUserDefaults.standardUserDefaults()
  
  keepalive = userdefaults.boolForKey("keepLiveOnBackground")
  //userdefaults.setBool(true, forKey: "keepLiveOnBackground")
}
```