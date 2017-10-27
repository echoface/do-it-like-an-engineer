# 单例的一种线程安全初始化

我们都看到过下面这样的单例初始化
```c
std::shared_ptr<some_resource> resource_ptr;
std::mutex mutex;
std::shared_ptr<some_resource> Instance() {
  std::unique_lock<std::mutex> lk(mutex);  //如果存在竞争，线程在此序列化等待 
  if(!resource_ptr) {
    resource_ptr.reset(new some_resource); 
  }
  lk.unlock();
  return resource_ptr;
  //resource_ptr->do_something();
}
```
这表现出了过度的线程安全；用力过猛之嫌；每个并发的访问都会有可能被等待，而然代码仅仅需要第一次去初始化了我们的一个对象而已；
之后应该也看到过所谓的`双重检查锁`的方案；
```c
  if(!resource_ptr) {
    std::lock_guard<std::mutex> lk(resource_mutex);
    if(!resource_ptr) {
      resource_ptr.reset(new some_resource);  // 3
    }
  }
  resource_ptr->do_something();  // 4
```
C++11 之后， 标准库里提供了`call_once`的选择让我们解决上面的问题；
```c
std::once_flag resource_flag;
std::call_once(resource_flag,funcion);
```
来提供线程安全的延迟初始化，就像chromium的base下的`base::LazyInstance`一样，只会在第一次使用的时候才会去做初始化；

如果全局只需要一个示例的情况下， 下面这种通过静态变量的方案可能是更好的一种选择；多线程可以安全高效的调用get_instance来获取数据，而不必当心多进程导致的竞争问题；
```c
class my_class;
my_class& get_instance() {
  static my_class instance;  // 线程安全的初始化过程
  return instance;
}
```