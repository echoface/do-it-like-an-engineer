# timegm implement

在android ndk中， timegm函数式没有在bionic中实现； man timegm给出的信息中， 给出了一个简易的timegm的实现；
原理：

> set the TZ environment variable to UTC, call mktime\(3\) and restore the value of TZ.

```c
time_t timegm(struct tm *tm)
{
    time_t ret;
    char *tz;

   tz = getenv("TZ");
    setenv("TZ", "", 1);
    tzset();
    ret = mktime(tm);
    if (tz)
        setenv("TZ", tz, 1);
    else
        unsetenv("TZ");
    tzset();
    return ret;
}
```


工作以来, 不管是看linux的代码还是看chromium的代码, 一直在感叹, 别人家的代码呀....\/苦笑

