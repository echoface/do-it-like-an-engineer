# futimes not find on NDK


简而言之，言而简之 就是ndk上没有提供这个非posix的函数， 用utimesat函数替代！

看stackflow： http://stackoverflow.com/questions/19374749/how-to-work-around-absence-of-futimes-in-android-ndk


futimes(3) is a non-POSIX function that takes a struct timeval (seconds, microseconds). The POSIX version is futimens(3), which takes a struct timespec (seconds, nanoseconds). The latter is available in bionic libc.

Update: I'm afraid I got a little ahead of myself. The code is checked into AOSP but isn't available yet.

However... if you look at the code, futimens(fd, times) is implemented as utimensat(fd, NULL, times, 0), where utimensat() is a Linux system call that does appear to be defined in the NDK. So you should be able to provide your own implementation of futimens() based on the syscall.

Update: It made it into bionic but not the NDK. Here's how to roll your own:
```c
// ----- utimensat.h -----
#include <sys/stat.h>
#ifdef __cplusplus
extern "C" {
#endif
int utimensat(int dirfd, const char *pathname,
        const struct timespec times[2], int flags);
int futimens(int fd, const struct timespec times[2]);
#ifdef __cplusplus
}
#endif

// ----- utimensat.c -----
#include <sys/syscall.h>
#include "utimensat.h"
int utimensat(int dirfd, const char *pathname,
        const struct timespec times[2], int flags) {
    return syscall(__NR_utimensat, dirfd, pathname, times, flags);
}
int futimens(int fd, const struct timespec times[2]) {
    return utimensat(fd, NULL, times, 0);
}
```
Add those to your project, include the utimensat.h header, and you should be good to go. Tested with NDK r9b.

(This should be wrapped with appropriate ifdefs (e.g. #ifndef HAVE_UTIMENSAT) so you can disable it when the NDK catches up.)

Update: AOSP change here.