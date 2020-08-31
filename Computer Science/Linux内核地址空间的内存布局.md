# Linux内核地址空间的内存分布及分配





![内核虚拟地址空间划分](/Users/xiao/huan/do-it-like-an-engineer/Computer Science/assets/27177626_135523006360CV.png)



> 896MB又可以细分为ZONE_DMA和ZONE_NORMAL区域。
> 低端内存(ZONE_DMA)：3G-3G+16M 用于DMA __pa线性映射
> 普通内存(ZONE_NORMAL)：3G+16M-3G+896M __pa线性映射 （若物理内存<896M，则分界点就在3G+实际内存）
> 高端内存(ZONE_HIGHMEM)：3G+896-4G 采用动态的分配方式



![映射关系](/Users/xiao/huan/do-it-like-an-engineer/Computer Science/assets/041141519417456.jpg)



![page分配调用链](/Users/xiao/huan/do-it-like-an-engineer/Computer Science/assets/20160929202400829.png)

## kmalloc/vmalloc

​	在设备驱动程序或者内核模块中动态开辟内存，不是用malloc，而是kmalloc ,vmalloc，释放内存用的是kfree,vfree，kmalloc函数返回的是虚拟地址(线性地址). kmalloc特殊之处在于它分配的内存是物理上连续的,这对于要进行DMA的设备十分重要. 而用vmalloc分配的内存只是线性地址连续,物理地址不一定连续,不能直接用于DMA。vmalloc函数的工作方式类似于kmalloc，只不过前者分配的内存虚拟地址是连续的，而物理地址则无需连 续。通过vmalloc获得的页必须一个一个地进行映射，效率不高， 因此，只在不得已(一般是为了获得大块内存)时使用。vmalloc函数返回一个指针，指向逻辑上连续的一块内存区，其大小至少为size。在发生错误 时，函数返回NULL。vmalloc可能睡眠，因此，不能从中断上下文中进行调用，也不能从其它不允许阻塞的情况下调用。要释放通过vmalloc所获 得的内存，应使用vfree函数, vmalloc和kmalloc的分配内存的特点大概如下：

![img](/Users/xiao/huan/do-it-like-an-engineer/Computer Science/assets/271601134697223.png)

区别大概可总结为：

- vmalloc分配的一般为高端内存，只有当内存不够的时候才分配低端内存；kmallco从低端内存分配(支持DMA)。
- vmalloc分配的物理地址一般不连续，而kmalloc分配的地址连续，两者分配的虚拟地址都是连续的；
- vmalloc分配的一般为大块内存，而kmaooc一般分配的为小块内存，（一般不超过128k);

kmalloc: 只能在低端内存区域分配(基于ZONE_NORMAL)，最大32个PAGE，共128K，kzalloc/kcalloc都是其变种
(slab.h中如果定义了KMALLOC_MAX_SIZE宏，那么可以达到8M或者更大)
vmalloc: 只能在高端内存区域分配(基于ZONE_HIGHMEM)
alloc_page: 可以在高端内存区域分配，也可以在低端内存区域分配，最大4M(2^(MAX_ORDER-1)个PAGE)
__get_free_page: 只能在低端内存区域分配，get_zeroed_page是其变种，基于alloc_page实现
ioremap是将已知的一段物理内存映射到虚拟地址空间，物理内存可以是片内控制器的寄存器起始地址，也可以是显卡外设上的显存，甚至是通过内核启动参数“mem=”预留的对内核内存管理器不可见的一段物理内存。

kmalloc和vmalloc申请的内存块大小是以字节为单位(实际上考虑到最小细分度，开辟的可能比申请的多，存在些许浪费)，而__get_free_page申请的内存块大小是以PAGE数量为单位。



