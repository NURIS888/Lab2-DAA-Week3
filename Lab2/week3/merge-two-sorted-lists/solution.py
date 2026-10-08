# Merge Two Sorted Lists
# https://leetcode.com/problems/merge-two-sorted-lists/

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def merge_two_lists(list1: ListNode, list2: ListNode) -> ListNode:
    """
    Merge two sorted linked lists into a single sorted linked list.

    Idea:
    Both lists are already sorted. Instead of building a brand-new list node
    by node with new values, I just re-link the existing nodes in the right
    order. I use a "dummy" head node so I don't have to special-case the
    very first node I attach — I always have something to point `.next` at.

    I keep two pointers, one for each list, and a "tail" pointer for the
    list I'm building. At every step I compare the current values of list1
    and list2, attach the smaller one to tail, and move that list's pointer
    forward. When one list runs out, whatever remains of the other list is
    already sorted, so I just attach it directly.
    """
    dummy = ListNode(-1)
    tail = dummy

    while list1 is not None and list2 is not None:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    # At most one of these is non-empty at this point.
    tail.next = list1 if list1 is not None else list2

    return dummy.next


# ---------- Helper functions used only for manual testing ----------

def build_linked_list(values):
    dummy = ListNode(-1)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def linked_list_to_list(head):
    result = []
    while head is not None:
        result.append(head.val)
        head = head.next
    return result


if __name__ == "__main__":
    test_cases = [
        ([1, 2, 4], [1, 3, 4]),
        ([], []),
        ([], [0]),
        ([5], [1, 2, 3]),
    ]

    for l1_vals, l2_vals in test_cases:
        l1 = build_linked_list(l1_vals)
        l2 = build_linked_list(l2_vals)
        merged = merge_two_lists(l1, l2)
        print(f"{l1_vals} + {l2_vals} -> {linked_list_to_list(merged)}")
