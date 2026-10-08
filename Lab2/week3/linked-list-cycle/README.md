# Linked List Cycle

LeetCode: https://leetcode.com/problems/linked-list-cycle/description/

## 1. Problem

I'm given the head of a linked list and I need to figure out whether the
list contains a **cycle** — meaning that at some point, following the
`.next` pointers long enough brings me back to a node I've already visited,
instead of eventually hitting `None`. I need to return `True` or `False`.
I'm specifically asked to do this **without using extra data structures**
that would cost O(n) space (like a hash set of visited nodes), if I want
the efficient solution.

## 2. Approach

I used **Floyd's Cycle Detection Algorithm**, also known as the
"tortoise and hare" approach.

The intuition: imagine two runners starting at the same point on a track.
One ("slow") moves 1 step at a time, the other ("fast") moves 2 steps at a
time.

- If the track is just a straight line with an end (no cycle), the fast
  runner reaches the end first and stops. They never meet again.
- If the track loops back on itself (there's a cycle), the fast runner
  will eventually "lap" the slow runner from behind, and at some point they
  will land on the exact same node at the exact same time.

So the algorithm is:
1. Start both `slow` and `fast` at `head`.
2. Loop while `fast` and `fast.next` are both not `None` (this condition
   protects against null pointer errors when fast tries to jump two steps).
3. Move `slow` forward by 1 node, and `fast` forward by 2 nodes.
4. If `slow is fast` (same node, not just same value), there is a cycle →
   return `True`.
5. If the loop exits normally (fast fell off the end of the list), there is
   no cycle → return `False`.

### Manual trace — case with a cycle

List: `3 -> 2 -> 0 -> -4`, and `-4`'s `.next` points back to `2` (index 1).

```
3 -> 2 -> 0 -> -4
     ^---------|
```

| Step | slow | fast |
|------|------|------|
| start | 3 | 3 |
| 1 | 2 | 0 |
| 2 | 0 | 2 (fast went -4 -> loop back to 2) |
| 3 | -4 | -4 |

At step 3, `slow` and `fast` are both at the node with value `-4` — same
object. The loop detects `slow is fast` and returns `True`.

### Manual trace — case without a cycle

List: `1 -> 2 -> 3 -> 4 -> 5 -> None`

| Step | slow | fast |
|------|------|------|
| start | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | 5 |
| 3 | 4 | fast.next is None → loop condition fails, exit |

The loop condition `fast is not None and fast.next is not None` becomes
false before `slow` and `fast` ever coincide, so the function returns
`False`.

Edge cases I checked:
- Empty list (`head = None`): the `while` condition is false immediately
  (`fast` is `None`), returns `False`.
- Single node, no cycle: `fast.next` is `None` right away, returns `False`.
- Single node pointing to itself (cycle of length 1): `fast` catches up to
  `slow` on the very first iteration.

## 3. Time Complexity

**Time Complexity: O(n)**, where `n` is the number of nodes in the list.

### Why

- **No-cycle case:** `fast` moves twice as fast as `slow`, so `fast`
  reaches the end of the list after roughly `n / 2` iterations of the
  loop. That's linear in `n`.
- **Cycle case:** once both pointers have entered the cycle, the distance
  between them (in terms of steps around the cycle) shrinks by 1 every
  iteration, because `fast` gains on `slow` at a rate of 1 extra step per
  iteration. Since the cycle length is at most `n`, the gap can be closed
  in at most `n` iterations. Combined with however many steps it took to
  *enter* the cycle in the first place (also at most `n`), the total
  number of iterations is still bounded by a constant multiple of `n`.

So in both cases, the number of loop iterations is proportional to `n`,
giving **O(n)** overall — each node is effectively "visited" only a small
constant number of times by either pointer, never revisited an unbounded
number of times.

**Space Complexity: O(1)**. I only use two extra pointer variables
(`slow` and `fast`), regardless of how long the list is. This is the key
advantage over the alternative "store visited nodes in a hash set"
approach, which would use O(n) extra space.

## 4. Reflection / Improvement

- Is there a more efficient approach? Not asymptotically — O(n) time is
  necessary, since in the worst case (no cycle) you must look at every
  node at least once to be sure there's no cycle; you can't skip any node
  and still be certain. So O(n) time is optimal.
- Could space be improved? Floyd's algorithm is already O(1) space, which
  is the best possible (you need at least a constant number of pointers
  to traverse the list at all). The brute-force alternative — keeping a
  hash set of every node visited and checking membership before each
  step — is also O(n) time, but O(n) space, so Floyd's two-pointer trick
  is the strict improvement over that brute-force version: same time
  complexity, better space complexity.
- Extension: this same technique (Floyd's) can be extended to not just
  detect a cycle but also find the **starting node** of the cycle (a
  follow-up version of this problem, "Linked List Cycle II"), by resetting
  one pointer to `head` after a collision and moving both one step at a
  time until they meet again. That part wasn't required here, but it's a
  natural next step built on the exact same two-pointer idea.
