# 单向链表的反转

假设有链表`0->1->2->3->4->5->6->7->8->9->null` 那么反转的结果就是 `9->8->7->6->5->4->3->2->1->0->null`


1.循环遍历
---

```c
struct Node {
    int data;
    Node* next;
};

Node* listReverse(Node* head) {
  Node* pre = NULL;
  Node* cur = head;
  while(cur != NULL) {
    Node* tmp = cur->next;
    cur->next = pre;
    pre = cur;
    cur = tmp;
  }
  return list_head = pre;
}
```

2. 递归实现
---
```c
struct Node {
  int val;
  Node* next;
  Node(int x): val(x),next(NULL) {}
};

struct Node* nullNode = new Node(0);

Node* reverse(Node* node) {

  if (node->next == NULL) {//list trail
    nullNode->next = node;
    return node;
  }

  //如果下个节点为真， 那就递归反转下个节点;
  Node* n = reverse(node->next);

  //返回下个节点， 那么就逆序将下个节点指向自己
  n->next = node;

  // 返回自己
  return node;
}
int main() {
  int arr[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
  int index = 0;
  Node* p = nullNode;
  while(index < 10) {
    p->next = new Node(arr[index]);
    p = p->next;
    index++;
  }
  p = nullNode;
  while(p = p->next)
    printf("%d-", p->val);
  printf("\n");

  Node* node = reverse(nullNode->next);
  node->next = NULL;

  p = nullNode;
  while(p = p->next)
    printf("%d-", p->val);
  printf("\n");
}

```