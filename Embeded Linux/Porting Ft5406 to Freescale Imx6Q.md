# 电容触摸屏FT5406移植说明

硬件连接：
---

  1.  触摸屏的电源VCC接到3.3V 
  2.  触摸屏的Reset上拉到10K电阻,后连接到一个GPIO 这里连接的是GPIO4_6
  3.  触摸屏的SDA和SCL接到FT5406的I2C接口 
  4.  INT接到IMX6Q的GPIO9.这是个支持中断的pin

> 说明：这个液晶屏是从迅为的三星4412板子上移植过来的，所以为了保证其性能和可靠性，我们使用了迅为那边的驱动，包括平台数据的移植; 更多的原理图相关的请查询5460的datasheet和相关的timming 图

移植步骤：
---

-  在arch/arm/mach-mx6/board-mx6q_sabresd.c文件中添加I2C设备.为了完成平台设备的初始化我们移植了itop4412上Ft5x06的平台数据结构
```c
/* add by Huan.Gong @2014/10/22 */
#ifdef CONFIG_TOUCHSCREEN_FT5X0X
#include <ft5x0x_touch.h>
static struct ft5x0x_i2c_platform_data ft5x0x_pdata = {
        .gpio_irq             = SABRESD_TS_INT ,
        .irq_cfg                = 0，
        .gpio_reset        = SABRESD_TS_RST,
        .screen_max_x   = 768,
        .screen_max_y   = 1024,
        .pressure_max   = 255,
};
#endif
/* end add */
```
- 将我们的触屏设备添加到I2C初始化数据结构中，并完成附上初始化数据参数
```c
static struct i2c_board_info __initdata mxc_i2c1_board_info[] = { 
   { 
        {       // add by Huan.Gong @ 2014/10/20
        	I2C_BOARD_INFO("ft5406_ts",0x38),
        .flags = 0,
        	.irq = gpio_to_irq(SABRESD_TS_INT),
        	.platform_data = &ft5x0x_pdata
        	},
};
```
    > 注：0x70是从设备的写地址，而设备地址是0x70的高7位，所以要向右移一位得到从设备地址得到0x38。 


 - 增加触摸屏引脚初化,在设备驱动程序中修改初始化的控制 主要时由三星的GPIO操作函数换成我们飞思卡尔平台的
```c
// capaticy touch srceen  gpio init 
static int __init ft5x0x_ts_init(void)
{
	int ret;
#define GTP_RST_PORT   IMX_GPIO_NR(4,6)
#define GTP_INT_PORT   IMX_GPIO_NR(1,9)
#define GTP_BLE_PORT   IMX_GPIO_NR(4,8)
#if 1
	printk("==%s: reset==\n", __FUNCTION__);
        ret = gpio_request(GTP_RST_PORT, "GPIO4_6");
        if (ret) {
                gpio_free(GTP_RST_PORT);
                ret = gpio_request(GTP_RST_PORT, "GPIO4_6");
                if(ret)
                {
                        printk("ft5xox: Failed to request GPIO4_6 \n");
                }
        }
        gpio_direction_output(GTP_RST_PORT, 0);
        mdelay(200);
        printk("ft5xox: set GPIO4_6 low 200ms reset the FT5406\n");
        gpio_direction_output(GTP_RST_PORT, 1);
        //s3c_gpio_cfgpin(EXYNOS4_GPX0(3), S3C_GPIO_OUTPUT);
        gpio_free(GTP_RST_PORT);
        msleep(10);
#endif
.........
```

- 将驱动文件ft5x06_ts.c和ft5x06_ts.h以及ft5x0x_touch.h文件在driver/input/touchscreen目录下 

在当前目录下，编辑Kconfig, 增加ft5x06驱动的配置选项 
```c
config TOUCHSCREEN_FT5X06 
   tristate 
    "FT5406 Touchscreen Interface" 
   depends on ARCH_AT91SAM9G45 || ARCH_AT91SAM9M10 
   default y 
   help 
     This enables support for the FT5X06 touchscreen interface. 
     The FT5X06 is multi-touch capacitive touch panel controller. 
     If unsure, say N (but it's safe to say "Y"). 
     To compile this driver as a module, choose M here; the module will be called ft5x06_ts 
```
- 在当前目录下，编辑Makefile，在文件最后一行添加： 

      obj-$(CONFIG_TOUCHSCREEN_FT5X06) += ft5x06_ts.o 

- 重新编译内核 Done!

//上面的基本上时移植整个驱动的步骤，但是实际移植中还是会碰到一些小问题，而这些小问题，如果不够细心，也不是那么容易被发现。

- 问题1：
  > 中断控制上的中断传递上，在前面的代码中我们可以看到，我们是在平台设备中提供的中断引脚给一个数据结构，那么通常，一个驱动的中断的申请和释放都是在驱动程序的初始化init 或者更多的是在probe中申请中断，在remove中释放中断的，而驱动设计的原则之中，就是将软硬件有一个很好的办法隔离，那么最好的办法就是在具体的plat_device和plat_driver中完成这些设备的引用和引脚的分配，之后通过数据结构指针将这些必要的信息提供给具体的设备驱动程序，那么驱动程序对应的处理就可以抛开硬件，只要关心传递过来的数据结构中的数据就行。于是我们在我们触屏的驱动的probe函数中看到了如下的代码：

```c
.............
	pdata = client->dev.platform_data;
	if (!pdata) {
		dev_err(&client->dev, "failed to get platform data\n");
		goto exit_no_pdata;
	}
	ts->screen_max_x = pdata->screen_max_x;
	ts->screen_max_y = pdata->screen_max_y;
	ts->pressure_max = pdata->pressure_max;
	ts->gpio_irq = pdata->gpio_irq;
	if (ts->gpio_irq != -EINVAL) {
		client->irq = gpio_to_irq(ts->gpio_irq);
	} else {
		goto exit_no_pdata;
	}
	// huan.gong
	if (pdata->irq_cfg) {
		    gpio_to_irq(pdata->irq);
	}
	ts->gpio_wakeup = pdata->gpio_wakeup;
	ts->gpio_reset = pdata->gpio_reset;
............
```

从这段代码中我们大致的可以看明白。就是我们在probe函数中申明了一个平台设备数据结构pdata，用来接收dev.platform_data数据结构，dev则是我们具体的I2C这个平台设备，当时我们在mach-imx6q_sabresd.c中初始化这个设备的时候提供了平台数据结构，现在在设备驱动程序中从新获取到这个数据结构，通过这个数据结构中的数据【事实上这些数据就是硬件的配置】来申请中断，配置中断，申请内核的一些其他必要的数据。这样就完成了设备的配置，而且做到了设备驱动和硬件的一种封装和隔离。

事实上在编译成功后，启动时发现log中报错了，说是request_irq失败，我们看看我们驱动的代码，其实感觉不出来哪里出错了，后来想到，linux下设备驱动对设备的占用情况，想到了，如果有一个驱动已经占用了这个设备或者占用了这个中断，当初始化我们的驱动的时候再次去申请使用这个中断当然就会失败了，想到这里，结合我们im6Q平台上的设备，很快就想到了可能是原来LCD的触屏IC tsc2007的驱动已经申请了这个中断并占用了，于是到mach-imx6q_sabresd.c中查看给I2C1上挂载的设备上果然有tsc2007，并且她的中断也是GPIO9这个脚的中断，于是屏蔽掉这段代码就成功的解决了这个问题。如下：
```c
static struct i2c_board_info mxc_i2c1_board_info[] __initdata = {
	{
		I2C_BOARD_INFO("mxc_hdmi_i2c", 0x50),
	},
	{
		I2C_BOARD_INFO("ov5640_mipi", 0x3c),
		.platform_data = (void *)&mipi_csi2_data,
	},
#if 0
	{
		I2C_BOARD_INFO("tsc2007", 0x4b),
		.type           = "tsc2007",
		.platform_data = &tsc2007_info,
		.irq = gpio_to_irq(SABRESD_TS_INT),
	},
#endif
#if 1
	// add by Huan.Gong @ 2014/10/20
	{
		I2C_BOARD_INFO("ft5406_ts",0x38),
		//.type = "ft5406_ts",
		//.addr = 0x38,
		.flags = 0,
		.irq = gpio_to_irq(SABRESD_TS_INT),
		.platform_data = &ft5x0x_pdata
	},
#endif
};
```

- 问题2：

在调试好之后，发现在触屏上XY的坐标是颠倒的，这个问题很快的就能定位到，时在上报触屏事件的时候，将x，y调换一下即可解决，通过查看代码，很容易就定位到了驱动中原本设计好的一个叫做swap_xy()这样一个函数。通过在事件上报前交换x-y就解决了这个问题。

- 问题3：
  NULL；

