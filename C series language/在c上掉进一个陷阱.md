# 我在C++上掉过的一个坑

其实没有掉下去，写c++代码，大多数时候都一直神经兮兮的，所以别的语言中不用脑袋思考的问题都会在cpp中小心翼翼，其实早就认为有问题了， 只是写了个小例子验证了下而已：

看下面的这样一段代码:

```c
std::set<Base*> container_;
void Base::doSomethingOnEachBase() {
    for (auto v : container_) {
        v->DoThings();
    }
}

void Base::DoThings() {
    //
    auto v = container_.find(this);
    container_.erase(v);
    //do other things    
}
```

上面的代码会发生crash， 这样看上去很明显问题出在哪里， 在一个for循环当中， 使用了迭代器，但是在这个循环当中， 我们从移除了当前的这个对象， 我想大多数人在阅读或者相关的网络上看到过下面这样的一个说明或者一个例子：
```C++
    for (iterator it = x.begain; it!= x.end(); it++) {
        it = it.erase(it);
    }
```
但是， 我们由`rang-based loop`中，这一切看上去都不会那么明显， 更重要的是， 在实际的工程中， 或者在复杂的多人合作项目中，这种事情变得更加隐晦， 我就是因为这样用了， 才由现在的教训；事实上， 我遇到的问题是因为我在循环中的好几层调用中的一个回调，在回调中因为对象不在需要被管理， 于是被移除掉了， 等回到这个for循环中，进行下一个循环时， crash了，而且从调用栈来看，就crash在for循环中， 但是单从这个`range-based loop`中， 我们基本上没办法确定这个问题；

    