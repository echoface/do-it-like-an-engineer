# 1. Two Sum


Given an array of integers, return **indices** of the two numbers such that they add up to a specific target.

You may assume that each input would have **_exactly_** one solution.

**Example:**  

<pre>
Given nums = [2, 7, 11, 15], target = 9,

Because nums[**0**] + nums[**1**] = 2 + 7 = 9,
return [**0**, **1**].
</pre>

就是给定一个整型数组，给定一个target整型数；要求找出数组中两个数相加等于给定的target；返回这两个数在数组中的索引；即`nums[i] + nums[j] == target`; 返回 `[i， j]`;

```c
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> v;
        for (int i = 0; i < nums.size() ; i++) {
            //if (nums[i] > target) { @01
                //continue;
            //}
            for (int j = i+1; j < nums.size(); j++) {
                //if (nums[j] > target) { @02
                    //continue;
                //}
                if (target == nums[i]+nums[j]) {
                    v.push_back(i), v.push_back(j);
                }
            }
        }
        return v;
    }
};
```
这个答案肯定是accept， 但是这样肯定不是最优的一个；{最烂的一个：800ms+ 哭晕呀....}后来考虑到了hashmap；c++11中有提供;于是又了下面这样的版本：13ms 靠！ 算法的威力呀.... 
```c
vector<int> twoSum(vector<int> &numbers, int target)
{
    //Key is the number and value is its index in the vector.
	unordered_map<int, int> hash;
	vector<int> result;
	for (int i = 0; i < numbers.size(); i++) {
		int numberToFind = target - numbers[i];

            //if numberToFind is found in map, return them
		if (hash.find(numberToFind) != hash.end()) {
			result.push_back(hash[numberToFind]);
			result.push_back(i);			
			return result;
		}
            //number was not found. Put it in the map.
		hash[numbers[i]] = i;
	}
	return result;
}
```


第一次做时， 在@01 @02位置加了条件， 缺乏考虑， 没考虑到负数的情况； 比如 `-3 + 4 = 1`; 我们不能因为 `4>1`就认为 4 与其它整数相加都大于1； so.....

第二个hashmap的是看到了别人的提示做的；原理就是，遍历数组；在hashmap中找目标值'target-nums[i]'，将遍历过且不是正确结果的值存入hashmap；而当我们找到这样的一个值时， 那么当前的索引i 和 hashmap中的索引就是我们要找的两个索引;

他人之言：
---

- > I submitted a method using unordered_map takes 20ms, but when I using binary search and std::sort, It only takes 12ms. What is the worst case means in unordered map?


- >Your answer seems O(n) but when I submitted your answer, the runtime was 20ms, which is worse than my answer of which the runtime is 16ms. My solution, However, is not O(n) but O(nlog(n)).And I checked out the site:
  > http://www.cplusplus.com/reference/unordered_map/unordered_map/find/

  > which shows that the complexity of find() is linear in worst case.



