# Ozone Overview

update: 使用online 版本的内容

Ozone is a platform abstraction layer beneath the Aura window system that is used for low level input and graphics. Once complete, the abstraction will support underlying systems ranging from embedded SoC targets to new X11-alternative window systems on Linux such as Wayland or Mir to bring up Aura Chromium by providing an implementation of the platform interface.

## Guiding Principles

Our goal is to enable chromium to be used in a wide variety of projects by making porting to new platforms easy. To support this goal, ozone follows the following principles:

1.  **Interfaces, not ifdefs**. Differences between platforms are handled by calling a platform-supplied object through an interface instead of using conditional compilation. Platform internals remain encapsulated, and the public interface acts as a firewall between the platform-neutral upper layers (aura, blink, content, etc) and the platform-specific lower layers. The platform layer is relatively centralized to minimize the number of places ports need to add code.
2.  **Flexible interfaces**. The platform interfaces should encapsulate just what chrome needs from the platform, with minimal constraints on the platform's implementation as well as minimal constraints on usage from upper layers. An overly prescriptive interface is less useful for porting because fewer ports will be able to use it unmodified. Another way of stating is that the platform layer should provide mechanism, not policy.
3.  **Runtime binding of platforms**. Avoiding conditional compilation in the upper layers allows us to build multiple platforms into one binary and bind them at runtime. We allow this and provide a command-line flag to select a platform (`--ozone-platform`) if multiple are enabled. Each platform has a unique build define (e.g. `ozone_platform_foo`) that can be turned on or off independently.
4.  **Easy out-of-tree platforms**. Most ports begin as forks. Some of them later merge their code upstream, others will have an extended life out of tree. This is OK, and we should make this process easy to encourage ports, and to encourage frequent gardening of chromium changes into the downstream project. If gardening an out-of-tree port is hard, then those projects will simply ship outdated and potentially insecure chromium-derived code to users. One way we support these projects is by providing a way to inject additional platforms into the build by only patching one `ozone_extra.gni` file.



more infomation ref:

[Ozone Overview](https://chromium.googlesource.com/chromium/src/+/60.0.3082.3/docs/ozone_overview.md)

