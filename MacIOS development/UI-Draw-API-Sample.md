# Draw API的使用和页面跳转

参看别人的做的， 但是那个博客中是通过静态cell，和viewcontroller进行连接的， 也就是一个cell 会connect 到一个storyboard中拖入的viewcontroller， 对于我这种内存恐惧症还是有蛮大的伤害的， 所以我自己改了改，新手、勿喷！

* #### storyboard 中是这样的

| ![](/MacIOS_development/img/drawAPIInNewViewController.png) |
| :---: |


* #### 运行成功后是这样子嘀

| ![](/MacIOS_development/img/运行效果.gif) |
| :---: |


* #### 很容易看明白吧， 就是在页面跳转的时候，通过函数将tableview中得数据传递到下一个要显示的page上。看代码：不得不赞一个apple公司在这函数和api的说明上写的非常cool

```swift
      // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
        let new_view = segue.destinationViewController as! PaletteViewController

        if let indexPath = self.tableView.indexPathForSelectedRow {
            switch indexPath.row {
            case 0:
                new_view.type = DrawType.Line
            case 1:
                new_view.type = DrawType.Rectangle
            case 2:
                new_view.type = DrawType.Circle
            default:
                new_view.type = nil
            }
            //let object : NSDictionary = listVideos[indexPath.row] as NSDictionary
            //(segue.destinationViewController as JieDetailViewController).detailItem = object
        }
    }
```

#### 在接收的那边， 收到类型之后根据不同的type绘制不同的形状就ok了,新建一个类binding到第二个页面中得view上；在drawapi来绘制不同的形状

```swift
import UIKit

class CanvasView: UIView {

    var drawtype:DrawType? = nil
    // *
    // Only override drawRect: if you perform custom drawing.
    // An empty implementation adversely affects performance during animation.
    override func drawRect(rect: CGRect) {
        print("I will Draw a \(drawtype!) here in size:width:\(rect.width),height:\(rect.height)")
        // Drawing code
    }
    //*/

    func drawLines() {
        print("i will draw lines here, but i gona sleep now")
    }
    func drawRectangle() {
        print("i will draw Rectangle here, but i gona sleep now")
    }
    func drawCircle() {
        print("i will draw Circle here, but i gona sleep now")
    }

}
```

---

### 再来看绘图 在ios中叫 core graphics

有时间先看看这篇文章：[http://www.cocoachina.com/industry/20140115/7703.html，](http://www.cocoachina.com/industry/20140115/7703.html，\)  看完之后应该不用说不会写代码了吧..\(_^__^_\) 嘻嘻……，

下面是其核心代码部分, 其中drawtype是通过prepareForSegue 函数传递过来的. 其中绘图的上下文通过  
_"UIGraphicsGetCurrentContext"_ 拿到, 这个上下文类似于javascript在浏览器中拿到的canvas.

其中core graphics 提供了一系列的函数来在特定的函数来完成基本的绘制  
 \(_^\_\_^\_\)

* CGPathMoveToPoint //将路径移动到一个点
* CGContextAddPath // 为上下文\(我更愿意称为canvas\) 添加一个CGPath来记录绘制的路径
* CGContextClosePath // 如果当前的路径不是一个闭合路径, 则添加直线将区域连成闭合区域 {3 -&gt; B }
* CGContextMoveToPoint //将绘制的路径开始点移动到一个指定点
* CGPathAddLineToPoint //在path路径中从当前位置开始链接一条线到指定点
* CGContextStrokePath // 按照path路径, 在canvas上画出这条线
* CGContextSetRGBStrokeColor // 设置画笔的颜色
* CGContextAddArc // 添加一个弧度角, 2\*pi当然就是一个圆啦
* CGContextSetLineWidth //设置线宽
* CGContextFillPath //填充路径, 要保证路径是closed 哦, 不然你看不到效果的
* CGContextAddEllipseInRect //添加一个椭圆,都说明了在矩形中啦, 请补习高中数学
* CGContextDrawImage // 绘制图像, 默认是颠倒的, 正过来的法方网上找
* CGContextSetRGBFillColor //设置田中的颜色
* CGContextSaveGState // 保存当前上下文状态, 因为有可能我们会拿这个canvas做变换,到时候我们绘制完我们的东西得还原回来, 不然, 呵呵, 你所有的绘制都不会是你想要的样子
* CGContextRestoreGState //不用说了吧, 看上一条
* ....

这一系列的基本函数来帮助我们完成图形的绘制,

```swift
    override func drawRect(rect: CGRect) {
        print("I will Draw a \(drawtype!) here in size:width:\(rect.width),height:\(rect.height)")
        if (nil == drawtype) {
            return
        }
        switch drawtype! {
        case DrawType.Line:
            self.drawLines()
        case DrawType.Rectangle:
            self.drawRectangle()
        case DrawType.Circle:
            self.drawCircle()
        case DrawType.Image:
            drawImage()
        case DrawType.Figure:
            PaiterBoard();
        }
        // Drawing code
    }


    override func touchesBegan(touches: Set<UITouch>, withEvent event: UIEvent?) {
        //let p = (touches as NSSet).anyObject()?.locationInview(self)
        let p = touches.first?.locationInView(self)
        CGPathMoveToPoint(path, nil, (p?.x)!, (p?.y)!)

        //(path, nil, touches.locationInView(self), )
    }

    override func touchesMoved(touches: Set<UITouch>, withEvent event: UIEvent?) {
        let p = touches.first?.locationInView(self)
        CGPathAddLineToPoint(path, nil, (p?.x)!, (p?.y)!)
        setNeedsDisplay();// 安排一次重绘
    }

    //*/
    func PaiterBoard() {
        print("i will draw when i move")
        let context = UIGraphicsGetCurrentContext()
        CGContextAddPath(context, path)
        CGContextStrokePath(context)
    }

    func drawLines() {
        print("i will draw lines here, but i gona sleep now")
        let context = UIGraphicsGetCurrentContext()
        CGContextMoveToPoint(context, 100, 100)
        CGContextAddLineToPoint(context, 100, 200)
        CGContextAddLineToPoint(context, 200, 200)

        CGContextSetRGBStrokeColor(context, 255, 0, 0, 1)
        CGContextStrokePath(context)


        //如果前面已经调用了 绘制的函数，比如CGContextStrokePath 下面就会失败，
        //相当于一个path已经被绘制了，就不在了
        CGContextClosePath(context) //当前path若不是闭合的，这个函数会添加一条直线让当前path闭合
        CGContextFillPath(context)
    }
    func drawRectangle() {
        let context = UIGraphicsGetCurrentContext()
        CGContextAddRect(context, CGRect(x: 110, y: 110, width: 40, height: 40))
        CGContextStrokePath(context)

        // 没有用，这里是fill，CGContextSetRGBStrokeColor(context, 255, 0, 0, 1)
        CGContextSetRGBFillColor(context, 255, 0, 0, 0.8)
        CGContextFillRect(context, CGRect(x: 200, y: 200, width: 40, height: 40))

        print("i will draw Rectangle here, but i gona sleep now")
    }
    func drawCircle() {
        let context = UIGraphicsGetCurrentContext()
        CGContextAddArc(context, 200, 200, 100, 0, 2*3.14, 0) //0: 顺时针, 1: 逆时针
        CGContextSetLineWidth(context, 6)
        CGContextStrokePath(context)
        CGContextAddArc(context, 200, 200, 90, 0, 2*3.14, 0) //0: 顺时针, 1: 逆时针
        CGContextFillPath(context) //填充

        //椭圆的方式来绘制圆
        CGContextAddEllipseInRect(context, CGRect(x: 100, y: 400, width: 100, height: 100))
        CGContextFillPath(context)

        //椭圆
        CGContextAddEllipseInRect(context, CGRect(x: 100, y: 600, width: 100, height: 50))
        CGContextFillPath(context)

        print("i will draw Circle here, but i gona sleep now")
    }

    func drawImage() {
        // UIImage(contentsOfFile: "") 这个借口不能用assets里面的资源,
        let img:UIImage? = UIImage(named: "xxx.png")
        let cgimg:CGImage? = img?.CGImage
        let context = UIGraphicsGetCurrentContext() //保存绘制前的状态
        CGContextSaveGState(context)//保存状态
        CGContextTranslateCTM(context, 10, 400)
        CGContextDrawImage(context, CGRect(x:100,y:100,width:300,height:300), cgimg)

        CGContextRestoreGState(context) //恢复之前的状态
    }
```

> ### 最后看一下storyboard中得样子, 还有一个最后完成的样子:

| ![](/MacIOS_development/img/手势绘图.gif) |
| :---: |


你以为是"你好"?? /奸笑

---

| ——**我就是code小兵，code小兵就是我** |
| ---: |




