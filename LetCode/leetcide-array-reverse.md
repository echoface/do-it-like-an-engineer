# 字符串数组的反序

example:
---

- input: `char* s = "IOU"; output: `UOI`


```c 
//O(N/2)
#include <stdio.h>

void reverse(char a[], int size) {
    int start = 0;
    int end = size-2; //ignore the '\0'
    while(start < end) {
        char t = a[start];
        a[start] = a[end];
        a[end] = t;

        start++;
        end--;
    }
}

int main() {
    char s[] = "hello,nice to meet you";
    printf("%s, size:%ld\n", s, sizeof(s));
    reverse(s, sizeof(s));
    printf("%s, size:%ld\n", s, sizeof(s));
}
```