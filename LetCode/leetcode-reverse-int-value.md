# 反序整型数

Reverse digits of an integer.

**Example1:** x =  123, return  321  
**Example2:** x = -123, return -321

[click to show spoilers.](https://leetcode.com/problems/reverse-integer/#)

**Have you thought about this?**

Here are some good questions to ask before coding. Bonus points for you if you have already thought through this!

If the integer's last digit is 0, what should the output be? ie, cases such as 10, 100.

Did you notice that the reversed integer might overflow? Assume the input is a 32-bit integer, then the reverse of 1000000003 overflows. How should you handle such cases?

For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows.

**<font color="red">Update (2014-11-10):</font>**  
Test cases had been added to test the overflow behavior.

```cpp

#include <limits>

class Solution { //6ms
public:
    int reverse(int x) {
        //bool is_negative = false;
        
        int max = 2147483647;
        int min = -2147483648;
        //std::cout << "max" << std::numeric_limits<int>::max();
        //std::cout << "min" << std::numeric_limits<int>::min();
        //if (x < 0) {
            //is_negative = true;
            //x = -x;
        //}
        long res = 0;
        do {
            res = 10*res+(x%10);
            x = x/10;
        } while(x);
        
        if (res > max || res < min)
            return 0;
        return (int)res;
    }
};
```