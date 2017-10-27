# three Sum

Given an array _S_ of _n_ integers, are there elements _a_, _b_, _c_ in _S_ such that _a_ + _b_ + _c_ = 0? Find all unique triplets in the array which gives the sum of zero.

**Note:** The solution set must not contain duplicate triplets.

<pre>
For example, given array S = [-1, 0, 1, 2, -1, -4],

A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
</pre>

看到这个题， 我立马想到了将公式拆解`a+b+c=0 ---> -a = b + c`;于是这样就可以用code01中的问题，可是， 尼玛...； 因为要去重， 我加了个排序， 结果很意外，超时了.... 呜呜.....;不仅仅有超时的问题；还有很多情况没考虑，比如说去重....; 长下面这样：
```c
#include <unordered_map>

class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int>> result;
        unordered_map<int, int> hash; //vector also ok;
        vector<int> item;
        
        sort(nums.begin(), nums.end());
        
        for (int i = 0; i < nums.size(); i++) {
            hash.clear();
            for (int j = i+1; j < nums.size(); j++) {
                int t = (-nums[i]) - nums[j];
                if (hash.find(t) != hash.end()) { //find it
                    item.push_back(nums[i]);
                    item.push_back(t);
                    item.push_back(nums[j]);
                    
                    if (find(result.begin(), result.end(), item) == result.end()) {
                        result.push_back(item);
                    }
                    item.clear();
                }
                //not find it
                hash[nums[j]] = j;
            }
        }
        return result;
    }
};
```

前前后后改了好多好多版本； 结果不是0去不掉， 就是把0全去掉了， 要么就是有重复， 抓狂......x2....x3;冷静下来， 冷静下来
```
［0,0,0,-1,-1, 2,2,2,-2,4,2,2,2,2,-4,1,-4,-4,0,0,0,1,1,0,1,-1］
/*
原本脑子里想的就是取出数组中的一个， 剩下的就变成两个数的和等于取出来的这个数的负数了；
可是题需要不能重复；既然要去重， 首先就是想到通过`sort(begin, end)升序` 之后通过
一些判断去掉重复的，a1, a2, a3来说，如果
*/
```

```c
#include <unordered_map>

class Solution {
public:
    
    vector<vector<int>> threeSum(vector<int>& nums) {
        vector<vector<int> > result;
        vector<int> v;

        if (nums.size() < 3)
            return result;

        sort(nums.begin(), nums.end());

        for (int t_index = 0; t_index < nums.size()-2; t_index++) {
            int target = 0 - nums[t_index];
            for (int i = t_index+1; i < nums.size() - 1; i++) {
                for (int j = i+1; j < nums.size(); j++) {
                    if (target == nums[i] + nums[j]) {
                        v.clear();
                        v.push_back(nums[t_index]);
                        v.push_back(nums[i]);
                        v.push_back(nums[j]);
                        result.push_back(v);
                    }
                    while(nums[j]==nums[j+1])
                        j++;
                }
                while(nums[i] == nums[i+1])
                    i++;
            }
            while(nums[t_index] == nums[t_index+1])
                t_index++;
        }
        return result;
    }
};
```