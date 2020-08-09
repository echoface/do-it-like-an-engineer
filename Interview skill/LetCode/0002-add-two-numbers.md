# Add Two Numbers

You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.


> 给你两个非负数链表， 数据的反序存放的【英语不好， 之前理解错了... 题目的意思是比如说1024 在数组中是4=&gt;2=&gt;0=&gt;1这样存放的意思】，把这两个数相加，并将结果放到一个链表中;

> Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
> Output: 7 -> 0 -> 8

其实理解了就好解决了， 遍历这个数组是免不了的了， 主要就是保存进位的问题， 还有两个数位数不等时补齐的问题;方法各种各样，我的办法是通过新建Node去补齐这部分， 其实可以不用这样做， 在循环中添加些判断就好了， 如果一个为NULL， 另一个非NULL的话， 结果就是非空的值就好了...;

方案1: 59ms
```
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        bool step_forward = false;
        if (l1 == NULL) return l2;
        if (l2 == NULL) return l1;
        
        ListNode* l1_node = l1;
        ListNode* l2_node = l2;
        while(l1_node != NULL && l2_node != NULL) {
            int sum = l1_node->val+l2_node->val + (step_forward ? 1 : 0);
            step_forward = sum > 9;
            l1_node->val = sum%10;
            //std::cout << l1_node->val << "-";
            if (l1_node->next == NULL && l2_node->next != NULL) {
                l1_node->next = new ListNode(0);
            } else if (l1_node->next != NULL && l2_node->next == NULL) {
                l2_node->next = new ListNode(0);
            } else if (l1_node->next == NULL && l2_node->next == NULL && step_forward) {
                l1_node->next = new ListNode(1);
            }
            l1_node = l1_node->next;
            l2_node = l2_node->next;
        }

        return l1;
    }
};
```

Note:
---

- 注意空值的判断
- 注意最后一个数相加后有进位的问题;


另一种尝试: 39ms
```c
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* addTwoNumbers(ListNode* l1, ListNode* l2) {
        bool step_forward = false;
        if (l1 == NULL) return l2;
        if (l2 == NULL) return l1;
        
        ListNode* l1_node = l1;
        ListNode* l2_node = l2;
        
        while(l1_node != NULL || l2_node != NULL) {
            
            if (l1_node && l2_node) {
                int sum = l1_node->val + l2_node->val + (step_forward ? 1 : 0);
                step_forward = sum > 9;
                l1_node->val = l2_node->val = sum%10;
                if (l1_node->next == NULL && l2_node->next == NULL && step_forward) {
                    l1_node->next = new ListNode(1);
                    return l1;
                }
                l1_node = l1_node->next;
                l2_node = l2_node->next;
                continue;
            } else if (l1_node == NULL) {
                int s = l2_node->val + (step_forward ? 1 : 0);
                l2_node->val = s % 10;
                step_forward = s > 9;
                if (step_forward == false) {
                    std::cout << "return l2" << std::endl;
                    return l2;
                }
                if (l2_node->next == NULL && step_forward) {
                    l2_node->next = new ListNode(1);
                    return l2;
                }
                l2_node = l2_node->next;
                continue;
            } else if (l2_node == NULL) {
                int s = l1_node->val + (step_forward ? 1 : 0);
                l1_node->val = s % 10;
                step_forward = s > 9;
                if (step_forward == false) {
                    std::cout << "return l1" << std::endl;
                    return l1;
                }
                if (l1_node->next == NULL && step_forward) {
                    l1_node->next = new ListNode(1);
                    return l1;
                }
                l1_node = l1_node->next;
                continue;
            }
        }
        return l1;
    }
};
```