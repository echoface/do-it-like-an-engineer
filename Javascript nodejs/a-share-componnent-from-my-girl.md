# Girl friend practice on js animation

先来👀一下效果图吧：

![](/assets/slideShareAnimation.gif)

看上去效果不错；虽然是基础，也算是对js和dom的积累和理解吧；

主要就是下面一些小的知识

* 通过js函数来改变box元素位置相关的样式来控制显示区域的大小
* 通过定时器函数`setInterval` 来控制动画的循环
* 完成点击时动作的触发

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <style>
        #box{

            height:200px;
            width:220px;
            position:relative;
            left:-208px;
        }
        #hide{
            height:200px;
            width:200px;
            background:blue;
            position:absolute;
            top:0;
        }
         span{
            height:50px;
            width:20px;
            background:red;
            position:absolute;
            left:200px;
            top:75px;
            cursor:pointer;
         }
        </style>
        <script>
            window.onload=function(){
                var button=document.getElementById("button");
                var flag=0;
                //鼠标单击分享时出现的移入和移出
               button.onclick=function(){
                    if(flag==0){
                         Move(40,0);
                         flag=1;
                    }else if(flag==1){
                        clearInterval(timer);
                        Move(-40,-200);
                        flag=0;
                    }
                }
                var timer=null;
                var speed,Target;

                var Move=function(speed,Target){

                    clearInterval(timer);
                    var hide=document.getElementById("hide");
                    var box=document.getElementById("box");
                    timer=setInterval(function(){
                        var speed=(Target-box.offsetLeft)/10;
                        speed=speed>0?Math.ceil(speed):Math.floor(speed);
                        if(box.offsetLeft==Target){
                            clearInterval(timer);
                        }else{
                             box.style.left=box.offsetLeft-8+speed+"px";
                             console.log(box.offsetLeft);
                        }
                    }, 20);

                }

                }
        </script>
    </head>
    <body>
    <div id="box">
    <div id="hide"></div>
    <span id="button">分享</span>
    </div>
    </body>
</html>
```

