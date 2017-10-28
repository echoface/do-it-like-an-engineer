# map_reduce_filter_sort

###map
map 就是将可映射的每个对象进行同一个函数的操作

```js
var arr = [0,1,2,3,4,5,6,7];
function add(x,y) {
  return x+y;
}
arr.map(add); // === 0+1+2+3+4+5+6+7
```
###Reduce
reduce 操作就是将一个可递归，可映射对象重复的利用某一个函数进行归并。函数的参数是上一次归并结果；

再看reduce的用法。Array的reduce()把一个函数作用在这个Array的[x1, x2, x3...]上，这个函数必须接收两个参数，reduce()把结果继续和序列的下一个元素做累积计算，其效果就是：

[x1, x2, x3, x4].reduce(f) = f(f(f(x1, x2), x3), x4)
比方说对一个Array求和，就可以用reduce实现：
```js
var arr = [1, 3, 5, 7, 9];
arr.reduce(function (x, y) {
    return x + y;
}); // 25
```