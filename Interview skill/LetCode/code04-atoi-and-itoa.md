# atoi 与 itoa 的实现

atoi
---

首先来看atoi，也就是说，要将一个以`\0`结束的`char*`字符串转化成ini型的值；首先想到的就是检测传入参数的合法性啦

```c
char* itostr(char *dest, size_t size, int a, int base) {
  static char buffer[sizeof a * CHAR_BIT + 1 + 1];
  static const char digits[36] = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  if (base < 2 || base > 36) {
    fprintf(stderr, "Invalid base");
    return NULL;
  }

  char* p = &buffer[sizeof(buffer) - 1];
  *p = '\0';

  int an = a < 0 ? a : -a;  

  // Works with negative `int`
  do {
    *(--p) = digits[-(an % base)];
    an /= base;
  } while (an);

  if (a < 0) {
    *(--p) = '-';
  }

  size_t size_used = &buffer[sizeof(buffer)] - p;
  if (size_used > size) {
    fprintf(stderr, "Scant buffer %zu > %zu", size_used , size);
    return NULL;
  }
  return memcpy(dest, p, size_used);
}

```