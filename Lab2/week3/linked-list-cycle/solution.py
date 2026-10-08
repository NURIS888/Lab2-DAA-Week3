# Linked List Cycle
# https://leetcode.com/problems/linked-list-cycle/

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def has_cycle(head: ListNode) -> bool:
    """
    Detect whether a linked list contains a cycle, using Floyd's
    "tortoise and hare" technique.

    Idea:
    I use two pointers that both start at head: 'slow' moves one node at a
    time, 'fast' moves two nodes at a time. Picture two runners on a track:
    if the track is a straight line (no cycle), the faster runner just
    reaches the end and stops — they never meet. If the track loops back
    on itself (a cycle), the faster runner eventually laps the slower one
    and they end up on the same node at the same time.

    So:
    - If fast (or fast.next) hits None, there's no cycle -> return False.
    - If at any point slow == fast (same node object), there is a cycle
      -> return True.
    """
    slow = head
    fast = head

    while fast is not None and fast.next is not None:
        slow = slow.next          # move 1 step
        fast = fast.next.next     # move 2 steps

        if slow is fast:
            return True

    return False


# ---------- Helper functions used only for manual testing ----------

def build_linked_list_with_cycle(values, pos):
    """
    Build a linked list from `values`. If pos >= 0, the tail of the list
    is connected back to the node at index `pos`, creating a cycle.
    pos = -1 means no cycle.
    """
    if not values:
        return None

    nodes = [ListNode(v) for v in values]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    if pos >= 0:
        nodes[-1].next = nodes[pos]

    return nodes[0]


if __name__ == "__main__":
    test_cases = [
        ([3, 2, 0, -4], 1, True),   # cycle back to index 1
        ([1, 2], 0, True),          # cycle back to index 0
        ([1], -1, False),           # single node, no cycle
        ([], -1, False),            # empty list
        ([1, 2, 3, 4, 5], -1, False),  # straight line, no cycle
    ]

    for values, pos, expected in test_cases:
        head = build_linked_list_with_cycle(values, pos)
        result = has_cycle(head)
        status = "OK" if result == expected else "FAIL"
        print(f"values={values}, pos={pos} -> has_cycle={result} (expected {expected}) [{status}]")
