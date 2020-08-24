# 树状数组(Binary Indexed Tree)

- 是什么

  一种方便求解区间数据和的数据结构. 其背后数据结构通过数组表示. 并有以下特征

  - C[i] 存储的值是SUM(A1, A2, ...Ai)的和
  - C[i] 管理存储的值和关系是通过lowbit(i)维护着的, lowbit(x)是x的二进制表达式中最低位的1所对应的值
    - C1(lowbit(1) = 1) 管理维护: A1(0001b)
    - C2(lowbit(2) = 2) 管理维护: A2(0010b), A1(0001b)
    - C3(lowbit(3) = 1) 管理维护: A3(0011b)
    - C4(lowbit(4) = 4) 管理维护: A4(0100b), A3(0011b), A2(0010b), A1(0001b)
    - C5(lowbit(5) = 1) 管理维护: A5(0101b)
    - C6(lowbit(6) = 2) 管理维护: A6(0110b), A5(0101b)
    - ....

- 为什么?有什么用

当需要求和Sum(A1....An)时, 我们只需要将转换后的很少一些C[i]节点相加即可.

![树状数组详细讲解，不会算法也能看懂哦~](/Users/xiao/huan/do-it-like-an-engineer/Computer Science/assets/v2-c57150473a48e2ce46e4a206da5fda21_1440w.jpg)



初始化:

```c
void BIT::init(int a[], int n) { // t is the BIT backend storage array
  for (int i = 1; i <= n; ++i) {
    t[i] += a[i];
    int j = i + lowbit(i);
    if (j <= n) t[j] += t[i];
  }
}


```

