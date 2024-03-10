为了家里网络的安全， 设置ssh listen on tailscale only;但是因为启动顺序的问题， ssh server 启动的时候tailscale网络并没有ready的情况下， 导致监听失败；同样的问题也发生在k8s对tailscale网络的依赖上;

在这种情况下，需要对systemd管理的服务进行启动顺序的编排；目前systemctl提供了`add-wants,add-requires`指令用于启动数据控制



```
systemctl add-wants kubelet.service tailscaled.service
# or
systemctl add-requires sshd.service tailscaled.service
```

