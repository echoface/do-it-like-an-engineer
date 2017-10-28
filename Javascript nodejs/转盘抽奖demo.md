＃ 转盘抽奖demo  纯js动画

👀 图：
![](/assets/lottery.gif)

下面几点是实现这个动作的key point：
---

* 设定当前选中☑️和普通没有高亮的css样式
* 通过数组定义转动的顺序
* 每次执行一个移动时，清楚当前样式-&gt; 计算出下个位置-&gt; 设置下个元素的样式
* 指定循环的速度改变策略
* 锁死开始按钮， 结束后恢复开始按钮
* `setTimeout` 和 使用随即生成的次数控制结束

几点没有做到的
---

实际应用中，这样可能是不行的／奸笑，还得控制概率的大小，而且最终的结果应该在服务器上做， 在浏览器中做这样的逻辑很容易被恶意js代码篡改掉

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        div{
            height:500px;
            width:500px;
        }
        li {
            height:100px;
            width:100px;
            background:pink;
            list-style:none;
            float:left;
            display:inline;
            margin:0 10px 10px 0;
            border:5px solid #ababab;
            text-align:center;
            line-height:100px;
            border-radius:20px;
        }
        .selected{
            filter:alpha(opacity=50);
            border:5px solid #0000ff;
            opacity:0.3;
            height:100px;
            width:100px;    
        }
        ul{ 
           float:left;
           display:inline;
           margin:0px;
        }
    </style>
</head>
<body>
    <div id="box">
        <ul id="box1">
            <li class="selected">iphone 4s</li>
            <li>iphone 5</li>
            <li>iphone 5s</li>

        </ul>
        <ul id="box2">
            <li>iphone 6</li> 
            <li onclick="start()">Start</li>
            <li>不要脸</li>
        </ul>
        <ul id="box3">
            <li>iphone 6p</li>
            <li>iphone 6s</li>
            <li>iphone 8s</li>

        </ul>
    </divi>
    <script>
        window.onload = function() {
            var items = document.getElementsByTagName("li");
            console.log(items.length)
            var i = 0;
            for (i = 0; i < items.length; i++) {
                items[i].index = i;
                console.log(items[i].index)
            }
        }
        function start() {
            var items = document.getElementsByTagName("li");
            items[4].onclick = undefined;
            items[4].innerHTML = "wait"

            var query = [0, 1, 2, 5, 8, 7, 6, 3];
            var query_index = 0;

            var loop_speed = 30; //ms
            var loop_times = GetRandomNum(24,56);  
            var times = makeIncreator();

            //preparation for start loop
            if (cur = document.getElementsByClassName("selected")) {
                for (i = 0; i < items.length; i++) {
                    if (items[i].className == "selected") { //find out current selected query index
                        query_index = i;
                        console.log("start from index:", i)
                        break;
                    }
                }
            } else {
                console.log("start from index:", 0)
                items[0].className = "selected";        
                query_index = 0;
            }

            function triggled() {
                items[query[query_index]].className = "";
                if (query[query_index+1]) {
                    query_index++;
                } else {
                    query_index = 0;
                }
                items[query[query_index]].className = "selected";

                var looped_times = times();
                if (looped_times > loop_times*2/3) {
                    loop_speed += 9;
                } else if (looped_times > loop_times/3) {
                    loop_speed += 6;
                } else {
                    loop_speed += 3;
                }
                if (loop_times > looped_times) {
                    setTimeout(triggled, loop_speed);
                } else {
                    items[4].innerHTML = "start"
                    items[4].onclick = start;
                }
            }
            setTimeout(triggled, loop_speed);

            function GetRandomNum(Min,Max) {   
                var Range = Max - Min;   
                var Rand = Math.random();   
                return(Min + Math.round(Rand * Range));   
            }
            function makeIncreator() {
                var i = 0;
                return function() {
                    return i++;
                }
            } 
        }
    </script>

</body>
</html>
```

