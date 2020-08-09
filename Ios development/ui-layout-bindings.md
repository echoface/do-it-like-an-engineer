## Layout && 匹配父级容器

**老的Xcode中是通过选中元素-&gt; 菜单editor -&gt; pin 来添加上下左右的边距来进行布局, 然后再属性页修改对应的值来改变layout**

新的Xcode中, 去掉了editor pin 的菜单选项, 而是添加了一个更加智能的选项, 看图

| ![](img/layout01.png) |
| :---: |

#### 经过上面的调整之后,我们看到的可以看到在documents outline 中多出了constraints的选项, 有上下左右四个子选项, 我们选中相应的项,修改值即可完成"匹配父级容器"操作

| ![](img/layout02.png) |
| :---: |


这样之后, 重新运行, 一起看起来都那么美好.....

查看apple官方的文档发现.原来的pin不是去掉了, 而是由editor菜单调整到了storyboard的视图上面;在storyboard中添加了新的功能选项来调整layout相关的功能;

| ![](img/layout03.png) |
|:--:|

