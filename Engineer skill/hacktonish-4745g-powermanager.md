# HackTonish_4745G_PowerManager


本帖最后由 s1025xfei 于 2014-2-4 21:15 编辑

---

在前人的帖子里面通过加载AppleLPC.kext来使用MAC原生的CPU电源管理 提到修改与苹果LPC设备匹配的ID来达到可以使用原生电源管理

所以呢，以后本论坛里面很多关于DSDT修改帖子里面都千篇一律的
如下写到

  查找：0x001F0000 或 Device (PX40)

加入（3A18）
xxxxxx
或加入（2815）
xxxxx

- 然后又不全面的提供完整的苹果LPC设备匹配的ID，导致太多人加入了（3A18）或者（2815）虽然可以加载AppleLPC.kext了。但是仍然无法使用原生电源管理，可能要用到破解的电源管理驱动AppleIntelCPUPowerManagement以加载来使用上原生电源管理，然后可以完美睡眠什么的。其实呢，修改DSDT之前每个人应该使用IORegistryExplorer搜索一下自己电脑的LPC的ID


- 比如我的就是pci8086,1c49，如果按照那些的修改DSDT帖子改成什么（3A18）或者（2815）就可能出现无法使用原生电源管理的情况。对此，我针对自己的情况修改成了
- 
```
Method (_DSM, 4, NotSerialized)
                {
                    Store (Package (0x02)
                        {
                            "device-id", 
                            Buffer (0x04)
                            {
                                0x49, 0x1C, 0x00, 0x00
                            }
                        }, Local0)
                    DTGP (Arg0, Arg1, Arg2, Arg3, RefOf (Local0))
                    Return (Local0)
                }
```

复制代码
实际上呢。在与苹果LPC设备匹配的ID列表里面就有我自己的ID。打开原生的AppleLPC.kext里面的info.plist文件，我们可以看得到与苹果LPC设备匹配的ID。
现在我提取的是10.9.1内置的最新的AppleLPC.kext(1.7.0)版本内置的ID列表，如果以后系统更新了，请各位自己去打开info.plist文件查找自己的主板ID是否在里面。
```
                                 pci8086,2811 
                                 pci8086,2815 
                                 pci8086,27b9 
                                 pci8086,27bd 
                                 pci8086,2670 
                                 pci8086,8119 
                                 pci8086,2916 
                                 pci8086,3a18 
                                 pci8086,3b00 
                                 pci8086,3b01 
                                 pci8086,3b02 
                                 pci8086,3b09 
                                 pci8086,1e44 
                                 pci8086,9c43 
                                 pci8086,9c43 
                                 pci8086,8c44 
                                 pci8086,8c4b 
                                 pci8086,1c42 
                                 pci8086,1c44 
                                 pci8086,1c4e 
                                 pci8086,1c4c 
                                 pci8086,1c50 
                                 pci8086,1c4a 
                                 pci8086,1c46 
                                 pci8086,1c5c 
                                 pci8086,1c52 
                                 pci8086,1c54 
                                 pci8086,1c56 
                                 pci8086,1c43 
                                 pci8086,1c4f 
                                 pci8086,1c47 
                                 pci8086,1c4b 
                                 pci8086,1c49 
                                 pci8086,1c41 
                                 pci8086,1c4d 
                                 pci8086,1d41 
                                 pci8086,1e42 
                                 pci8086,1e55 
                                 pci8086,1e58 
                                 pci8086,1e57 
                                 pci8086,1e59 
                                 pci8086,1e5d 
                                 pci8086,1e43 
                                 pci8086,1e56 
                        
```
复制代码
这样改下来保存好DSDT部分人ID在这个列表里面的就可以通过加载AppleLPC.kext来使用MAC原生的CPU电源管理而不需要破解的电源管理补丁了。

 - 查看自己主板的LPC的ID除了使用IORegistryExplorer，还可以使用Systeminfo MAC版本（需要java支持），可以用DPCIManager 查看id（感谢14f推荐），还有在windows 下打开设备管理器，展开系统设备，在里面可以看到LPC的ID。一般在最后面，如果mac下的ID和windows下不一样，以windows中看到的为准。


 - 你的ID一定要在 本文的列表中才有效，否则按照7F的方法去试试看添加修改
修改后查看是否加载了加载AppleLPC.kext，如果加载了，正常情况下是可以加载最新版本的原生电源管理驱动的，但是也有可能无法加载，请使用破解版本的或者老版本的电源管理驱动试试看。还不行的话clover添加AsusAICPUPM=Yes或者刷修改版本的BIOS
本文所需下载的东西请点文中链接，改了之后有效果的请点赞。




 - LPC的id也可以在Windows的设备管理器里的LPC Controller里查看哦。另外，如果自己的id不在支持列表里，不建议把自己的id加进info.plist里，以加载AppleLPC，因为这样虽然能够加载AppleLPC，但这应该是空加载，实际这样并不会调用AppleLPC的二进制程序，而只是加载了AppleLPC的空壳。
    个人觉得，如果自己的id不在支持列表里，就选择支持列表里与自己的最接近的加入DSDT，比如，先看看有没有id的前三位都一样的，没有的话选前两位一样的。这样，加载AppleLPC应该就能调用实际的程序了。
    当然，如果用接近的无效，最后的方法，还是把自己电脑的id加到AppleLPC的info.plist里。另，祝新年快乐。

> reference: http://bbs.pcbeta.com/viewthread-1473630-1-1.html

//**File End**