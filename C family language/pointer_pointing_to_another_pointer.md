#pointer pointing to another pointer

在看大型C工程的时候，经常能看到char \*\* 甚至 void \*\*这样指向指针的指针，有很多人都不明白，为什么要非得用指向指针的指针

其实总结起来，如果你在函数外定义的指针有内容，或者这个内容只是供调用他的函数使用 ，那么你完全没有必要使用void \*\*这样的方式来访问你的数据，只需要void \* 这样的指针就行了，但是当我们需要在函数内部修改外部指针时，那么这时候就显的尤为必要
了，总的来说，使用void \*\* 是因为我没要修改或使用指针，而不仅仅使用指针指向的数据。比如我们看个例子来说明下：

假如我们使用指针作为参数传递给一个函数,并希望返回新的指针值，这个时候是错误的
```C
char* ptr = NULL;
function(char* p)
{
    p = malloc(1024);
    //p的内容为1024个字节的内存起始地址
}
```
//但是执行到这里的时候依然是 ptr == NULL;
//并不是我想要得到的结果，说到底，这也是个变量

只有使用指针的指针才可以实现返回新的指针
```C
char* ptr = NULL;
char** pp= &ptr;
   int function(char** pp)
  {
    *pp = malloc(1024);
      //*pp的内容为1024个字节的内存起始地址
  }
//执行到这里的时候 *pp的内容仍然为ptr的地址;
//但是*ptr的内容已经指向了新分配的1024的内存空间
```

上面的例子可能只是说明性的例子，可能还是没有足够的说服力，来让你相信有时候没有指向指针的指针还真的不好办！
比如在V4l2应用中的代码：
```c
int catch_Oneframe(uchar **p_fram,__u32 *fameSize) {
    struct v4l2_buffer buf;
    CLEAR (buf);
    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    buf.memory = V4L2_MEMORY_MMAP;

    if (-1 == xioctl(m_cameraFd, VIDIOC_DQBUF, &buf)) {
        switch (errno) {
            case EAGAIN:
                return 0;
            case EIO:
                /* Could ignore EIO, see spec. */
                /* fall through */
            default:
                errno_exit("VIDIOC_DQBUF");
        }
    }
    else
    {
        assert(buf.index < n_buffers);
        (*p_fram) = (uchar *)buffers[buf.index].start;
        *fameSize = buffers[buf.index].length;
        //qDebug() << "imagesize is" << framSize << "\n";
    }
    return SUCCESS;
}
```
这段代码中我们希望通过在函数外申明一个uchar \*fram的指针来指向我们要获取的一帧图像，之后申明了一个表示这个图像的大小的int 型变量。而返回值表示我们到底时成功了还是失败了。所以实际看到的应用是这样的：
```c
uchar *p_fram = NULL;
unsigned int size = 0,ret = 0;
ret = catch_Onefram(&p_fram,&size);
if(ret)   
  transform(p_fram,size);
  //do other img processing 
  else 
  //return false
```
有的人会问，可以把函数改写成返回指针的形式呀，yes，是的可以这样做，比如改写成这样：

    uchar * catch_Oneframe(int *return_value,__u32 *fameSize)；

这样改写函数本身是没有错误的，并且能够正常的工作，但是在C语言编程时保持链式表达的支持，这样写会有好处的比如说：
```c
uchar *p_fram = NULL;
unsigned int size = 0,ret = 0;
if(catch_Onefram(&p_fram,&size))
  transform(p_fram,size);
  //do other img processing
else
  //return false
```
have a nice day！ Huan.Gong

