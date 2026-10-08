# Merge Two Sorted Lists

LeetCode: https://leetcode.com/problems/merge-two-sorted-lists/description/

## 1. Problem

I'm given two linked lists, and each one is already sorted in non-decreasing
order. I need to combine them into **one** sorted linked list and return its
head. I'm not allowed to just dump everything into an array, sort it, and
rebuild a list — the point is to merge the two lists directly by relinking
nodes (or at least that's the efficient/expected way to do it).

## 2. Approach

This is basically the "merge" step from merge sort, applied directly to
linked lists instead of arrays.

Since both lists are sorted, the overall smallest remaining element is
always either the current head of `list1` or the current head of `list2`.
So I can walk through both lists at the same time with two pointers, always
picking the smaller of the two current nodes, attaching it to my result,
and advancing only the pointer I picked from.

To avoid writing special-case code for "what is the very first node of the
result", I use a **dummy node** trick: I create a fake `ListNode(-1)` node
that isn't part of the final answer, and I always attach new nodes after a
`tail` pointer that starts at `dummy`. At the end, the real answer starts at
`dummy.next`.

Steps:
1. Create `dummy` and set `tail = dummy`.
2. While both `list1` and `list2` still have nodes left:
   - Compare `list1.val` and `list2.val`.
   - Attach the smaller node to `tail.next`, then move that list's pointer
     forward (`list1 = list1.next` or `list2 = list2.next`).
   - Move `tail` forward to the node I just attached.
3. When the loop ends, one of the lists is empty and the other one still
   has some nodes left — but since it was already sorted, I can just attach
   it as-is to `tail.next`. No more comparisons are needed.
4. Return `dummy.next`.

### Manual trace

Example: `list1 = [1, 2, 4]`, `list2 = [1, 3, 4]`

Start: `dummy -> None`, `tail = dummy`

| Step | list1 head | list2 head | Comparison | Attach | tail now points to | list1 after | list2 after |
|------|-----------|-----------|------------|--------|---------------------|-------------|-------------|
| 1 | 1 | 1 | 1 <= 1 → take list1 | 1 (from list1) | node(1) | [2,4] | [1,3,4] |
| 2 | 2 | 1 | 2 <= 1 is false → take list2 | 1 (from list2) | node(1) | [2,4] | [3,4] |
| 3 | 2 | 3 | 2 <= 3 → take list1 | 2 | node(2) | [4] | [3,4] |
| 4 | 4 | 3 | 4 <= 3 is false → take list2 | 3 | node(3) | [4] | [4] |
| 5 | 4 | 4 | 4 <= 4 → take list1 | 4 | node(4) | [] | [4] |

Now `list1` is empty, loop stops. Remaining `list2 = [4]` gets attached
directly to `tail.next`.

Final result: `dummy.next = 1 -> 1 -> 2 -> 3 -> 4 -> 4`, which matches
LeetCode's expected output for this example.

Edge cases I specifically checked:
- Both lists empty → returns `None` (an empty list).
- One list empty → the loop body never runs, and the non-empty list is
  attached whole at the end.

## 3. Time Complexity

**Time Complexity: O(n + m)**, where `n` and `m` are the lengths of
`list1` and `list2`.

### Why

Every iteration of the `while` loop consumes exactly one node — either from
`list1` or from `list2` — and advances that list's pointer. A node is never
visited twice and never "put back." So the loop can run at most
`n + m` times before at least one of the lists is exhausted. After the
loop, attaching the leftover tail is O(1) (it's just one pointer
assignment, not a node-by-node copy, since I reuse existing nodes). So the
total work is proportional to the combined length of both lists:
**O(n + m)**.

**Space Complexity: O(1)** extra space (not counting the output list
itself). I'm not allocating new nodes for the values — I'm re-using the
existing nodes from `list1` and `list2` and just rewiring their `.next`
pointers. The only extra memory is a fixed number of pointers (`dummy`,
`tail`, and the loop uses the input pointers themselves), regardless of
how long the lists are.

## 4. Reflection / Improvement

- Is there a more efficient approach? Not really, in terms of asymptotic
  complexity — O(n + m) is already optimal, because any correct algorithm
  has to at least look at every node once to decide where it belongs in
  the output. You can't do better than linear time here.
- What could be changed? The main alternative is a **recursive** version of
  the same idea (compare heads, recurse on the rest, attach the smaller
  one). It's arguably more elegant to read, but it has the same O(n + m)
  time complexity and actually uses **O(n + m) space** instead of O(1),
  because of the call stack depth from recursion. So my iterative version
  is actually the more space-efficient of the two — I'd only prefer the
  recursive version for readability, not performance.
- If this were extended to merging **k** sorted lists instead of 2, the
  naive way of repeatedly merging two lists at a time would cost
  O(k · n) in the worst case. A better approach there would be to use a
  min-heap of size `k` (always pop the smallest head among all k lists),
  which would bring it down to O(n log k). That's outside the scope of
  this specific problem, but it's the natural generalization.
