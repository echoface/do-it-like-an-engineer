# Get Ip/gateway/dns throgh sh script On Platform Linux(Unix)

- replace "br0" by your network hardware name. 

```sh
        #!/bin/bash
         
        #本脚本是获取计算机当前的网络配置信息
        #注意下面的'br0'需要根据个人的网络适配器名称来进行修改
        
        #1、获取ip地址
         
        echo "获取当前的ip地址是："
        #第一种方法
        ifconfig br0 |grep "inet addr:" |sed 's/.*addr://g'|sed 's/Bcast.*$//g'
        #第二种方法
        #ifconfig br0 |grep "inet addr:" |sed 's/.*addr://g' |awk '{print $1}'
         
        #2、获取子网掩码
        echo "获取当前的子网掩码："
         
        ifconfig br0 |grep "inet addr" |awk 'BEGIN{FS=":"}{print $4}'
         
        #3、获取网关
        echo "获取当前的网关："
         
        route -n |grep "UG" |awk '{print $2}'
         
        #4、获取DNS
        echo "获取当计算机的DNS地址："
         
        cat /etc/resolv.conf |grep "nameserver"|awk '{print $2}'
         
        #5、获取MAC地址
        echo "获取当前适配器的MAC地址:"
         
        ifconfig |grep "^br0" |awk '{print $5}'
```


---
