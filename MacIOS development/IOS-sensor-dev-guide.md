# 各类系统传感器的使用

加速度计 acceleration
---

各个轴方向上得加速度大小



陀螺仪 gyroscope
---

各个方向的角速度..... 


电源电池状态 PowerMonitor
---

通过notifycationCenter 添加observer 侦听状态变化即可



红外距离传感器 ProximityMonitor
---

类似于电池侦听, 通过notifycationCenter 添加observer侦听状态变化, 两个状态, true/false




磁场传感器(方向传感器,指南针) Magnetic
---

- import CoreLocation 导入Corelocation 基础类
- 获取lm = CLLocationManager() 获取loction manager
- 继承,实现CLLocationManagerDelegate 协议
- lm.startUpdatingHeading 开始侦听方向变化
- override didupdateHeading 方法来获取方向变化


全球定位系统GPS 
---

类似于磁场传感器