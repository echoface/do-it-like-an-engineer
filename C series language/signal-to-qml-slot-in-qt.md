# C++ SIGNAL to QML SLOT in Qt

在qt的MetaObject的支持下, 我们可以方便的完成QML和C++的交互, 而QML在C++中没一个版本的变化都挺大的. 有很多中方法来支持C++和QML的交互; 具体可以参考QT的官方文档,{吐槽一下: 现在qt的文档越来越跟不上版本和代码的变更了}

[QT Documents](http://doc.qt.io/qt-5/qtqml-cppintegration-interactqmlfromcpp.html)

导出C++类到QML上下文中
---

这里讲到的是我们如何将我们C++类中得信号,导出到QML中, 按照Qt官方的说法,在MetaObject的支持向, 理论上不管是C++　还是QML中得信号, 都是可以connect的, 可这是理论上呀{哭晕...};
看下面的代码:
```javascript
Item {
  objectName: ""
  Connections {
      target: MetaObject // namely QOBJECT 
      onAxxxsignal: {
        objectName = sinal_arguments
      }
  }
}
```
一个直接的问题, 如果这个metaobject是一个c++对象, 在qml中如何拿到这个对象呢? 在最新的Qt5.1+的版本中, 用子类QQmlApplicationEngine代替了QQmlEngine, 这个QQmlApplicationEngine变成了整个qml执行环境的完整上下文, 它继承了QObject, QQmlEngine, QJSEngine; 通过它可以取到qml对象的QQmlContext,RootObject等等对象;
具体参考:[](http://doc.qt.io/qt-5/qqmlapplicationengine.html)

要想在QML中访问C++对象, 按照下面的步骤即可将QObject对象暴露到qml中:

- 1. 实现自己的类, 必须继承自Qobject类;这是Qt本身机制所必须得
- 2. 通过QQmlApplicationEngine 获取到 QQmlContext对象, 它提供了直接的借口来get到这个上下文环境
- 3. 通过Context()->setContextProperty("YourObject", myOb);来将你的对象暴露给QML
- 4. 在qml中直接使用YourObject对象即可;

  > 信号和槽本身是整个qt中qml 和 qt/C++ 共同的机制, 所以一旦将你设计的类暴露出去之后, 你的类所拥有的信号和槽本身就已经暴露出去了; QML中直接使用 YourObject.yoursignal(); YourObject.youSlot(); 都是可以的;当然也可以使用信号来连接到其他对象[不管是c++的还是qml的]槽上, 或者将其他信号连接到yourobject的slot上

所以上面说的这些就可以用下面的代码来实现:

```c++
sinal c++Signal(QString singalString);
...
QString objproperty = "XReaderContext";
QQmlContext* qml_context = m_engine->rootContext();
qml_context->setContextProperty(objproperty,this);
```
```javascript
//qml中
Connections {
    target: XReaderContext 
    onC++Signal: {
        qmlString = signalString
    }
}
```

同样的, 如果你需要将qml对象的信号, 连接到C++ Object的slot上, 可以在这个模块OnLoadCompleted:中利用 signal.conect(C++object, slotfunction)来完成绑定

QML 中调用 C++ 中得public方法
---

在整合C++/QML的过程中, 通过导出C++对象, 好像基本可以完成大部分工作了, 但是还有一个问题: 如何调用C++对象的方法;
当然这其中有折中的方法, 就是通过C++的槽, qml中信号连接到C++对象的槽上, 之后通过信号触发槽函数的执行, 在槽中再调用我们的C++对象的函数; 想我这种效率恐惧症是接受不了这样绕弯的方法的, 当然, 除非出于设计结构或者其他更重要的原因;

其实很简单, 要暴露我们的类成员方法到qml执行环境中, 只需要通过宏**Q_INVOKABLE**标识即可;比如:
        
        Q_INVOKABLE int gu(int size)
这样就可以在上面导出C++对象到qml上下文中的基础上, 直接在qml中调用我们导出的普通C++成员函数或者成员变量了;
        
        //qml中
        YourC++Object.gu(10);
同样地实现机制,我们可以通过宏**Q_PROPERTY**来将c++的成员变量暴露到qml上下文环境中;
        
        Q_PROPERTY(QString author READ author WRITE setAuthor NOTIFY authorChanged)

具体去看看qt的文档即可!
参考: 
- [signal-to-qml-slot-in-qt](http://stackoverflow.com/questions/8834147/c-signal-to-qml-slot-in-qt)
- [qtqml-cppintegration-interactqmlfromcpp](http://doc.qt.io/qt-5/qtqml-cppintegration-interactqmlfromcpp.html)
- [qtqml-cppintegration-exposecppattributes](http://doc.qt.io/qt-5/qtqml-cppintegration-exposecppattributes.html)
- [connecting-c-with-qml-using-q-invokable](http://stackoverflow.com/questions/9341005/connecting-c-with-qml-using-q-invokable)