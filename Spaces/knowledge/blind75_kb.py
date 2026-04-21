"""
knowledge/blind75_kb.py
────────────────────────
The AlgoSensei knowledge base.

Contains original pattern explanations written for this system, drawing on
concepts from Introduction to Algorithms (CLRS), MIT OCW 6.006, and
Stanford CS161. Each entry is a self-contained chunk suitable for RAG retrieval.

Structure per pattern:
  - concept:    what the pattern is and why it exists
  - intuition:  the core mental model (analogy-first)
  - mechanics:  how to recognize and apply it
  - complexity: time and space analysis
  - pitfalls:   common mistakes
  - problems:   which Blind 75 problems use this pattern
"""

KNOWLEDGE_BASE = [

    # ══════════════════════════════════════════════════════════
    # PATTERN 1: ARRAYS & HASHING
    # ══════════════════════════════════════════════════════════
    {
        "id": "arrays_hashing_concept",
        "pattern": "arrays_hashing",
        "topic": "concept",
        "text": """Arrays and hash maps are the foundation of nearly every efficient algorithm.
An array gives O(1) random access by index. A hash map gives O(1) average-case
lookup, insertion, and deletion by key. Together they let you trade space for time:
instead of scanning an array repeatedly (O(n) per scan), you build a hash map once
(O(n)) and answer future queries in O(1). This is the fundamental space-time tradeoff
in algorithm design. Source: CLRS Chapter 11 — Hash Tables.""",
    },
    {
        "id": "arrays_hashing_intuition",
        "pattern": "arrays_hashing",
        "topic": "intuition",
        "text": """Think of a hash map as a coat check at a restaurant. When you arrive, you hand
over your coat and receive a ticket number. When you want your coat back, you hand
over the ticket and get it immediately — no searching through every coat. The ticket
number is the hash of your key; the coat rack position is the bucket. You traded a
small amount of space (the ticket system) to eliminate the need to search. This is
exactly what Two Sum does: instead of checking every pair (O(n²)), you store each
number's complement in a hash map as you scan, retrieving it in O(1) when you find
the match. Source: MIT OCW 6.006 Lecture 8.""",
    },
    {
        "id": "arrays_hashing_mechanics",
        "pattern": "arrays_hashing",
        "topic": "mechanics",
        "text": """Recognize array/hashing problems by these signals: the problem asks about pairs,
complements, duplicates, or frequencies. The brute force is O(n²) with nested loops.
The key insight is always: 'what information do I need to remember from elements I've
already seen?' That remembered information goes into a hash map. Canonical setup:
scan left to right, check if current element's complement/pair is already in the map,
if not add current element to the map. For frequency problems, use a Counter or
defaultdict. For duplicate detection, use a set. Source: Stanford CS161 — Problem
Set 1.""",
    },
    {
        "id": "arrays_hashing_complexity",
        "pattern": "arrays_hashing",
        "topic": "complexity",
        "text": """Hash map operations (insert, lookup, delete) are O(1) average case due to
hashing, but O(n) worst case due to collisions. In practice with a good hash function
the average case holds. Space complexity is O(n) to store at most n entries.
The total algorithm is O(n) time, O(n) space — an improvement over the naive O(n²)
time, O(1) space brute force. This tradeoff (linear space for linear time) is almost
always worth it in interview problems. Source: CLRS Section 11.2.""",
    },
    {
        "id": "arrays_hashing_pitfalls",
        "pattern": "arrays_hashing",
        "topic": "pitfalls",
        "text": """Common mistakes with hash map problems: (1) Adding the current element to the
map before checking it — for Two Sum this causes using the same element twice.
Always check first, then add. (2) Confusing set (membership) with dict (key→value).
Use a set when you only need to know if something exists; use a dict when you need
to store associated information like an index. (3) Forgetting that hash maps have
O(n) worst-case due to collision — mention this in interviews to show awareness.
Source: CLRS Section 11.4 — Open Addressing.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 2: TWO POINTERS
    # ══════════════════════════════════════════════════════════
    {
        "id": "two_pointers_concept",
        "pattern": "two_pointers",
        "topic": "concept",
        "text": """Two pointers is a technique for reducing nested loops to a single pass by
maintaining two indices that move through the array in a coordinated way. When the
array is sorted (or can be sorted), two pointers can replace O(n²) brute force with
O(n) scanning. The pointers typically start at opposite ends and converge, or start
together and expand. The key insight: sorting destroys index information but preserves
value relationships, and many problems only care about values. Source: CLRS Chapter
2 — Sorting and Order Statistics.""",
    },
    {
        "id": "two_pointers_intuition",
        "pattern": "two_pointers",
        "topic": "intuition",
        "text": """Imagine filling a container with water using two walls. The water level is
determined by the shorter wall — raising the taller wall does nothing; you must raise
the shorter wall to potentially increase the volume. This is exactly Container With
Most Water: move the pointer at the shorter wall inward, because moving the taller
wall can only decrease or maintain the width while not improving the height. The two
pointers represent competing constraints that need to be balanced. Sort first, then
the sorted order tells you which direction to move each pointer. Source: MIT OCW
6.006 Lecture 3.""",
    },
    {
        "id": "two_pointers_mechanics",
        "pattern": "two_pointers",
        "topic": "mechanics",
        "text": """Recognize two-pointer problems: sorted array, looking for a pair or triplet
satisfying a condition, palindrome checking. Setup: sort if needed, place left=0 and
right=len-1. Move pointers based on comparison to target: if sum < target, move left
right (increase sum); if sum > target, move right left (decrease sum). For 3Sum, fix
one element with an outer loop and run two pointers on the rest. Skip duplicates by
advancing pointers past repeated values. The pattern eliminates one dimension of
the search space per step. Source: Stanford CS161 — Two-Pointer Technique.""",
    },
    {
        "id": "two_pointers_complexity",
        "pattern": "two_pointers",
        "topic": "complexity",
        "text": """Two pointers after sorting: O(n log n) for the sort dominates, O(n) for the
scan. Total: O(n log n) time, O(1) extra space (ignoring sort stack). For 3Sum, the
outer loop adds one factor of n, giving O(n²) time. Compare to brute force O(n³) for
3Sum — two pointers provide one order of magnitude improvement. The space
efficiency (O(1) extra) is the main advantage over hash map approaches for sorted
input. Source: CLRS Section 2.3.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 3: SLIDING WINDOW
    # ══════════════════════════════════════════════════════════
    {
        "id": "sliding_window_concept",
        "pattern": "sliding_window",
        "topic": "concept",
        "text": """Sliding window maintains a contiguous subarray (the 'window') that satisfies
some condition, expanding the right boundary to add elements and shrinking the left
boundary to remove elements. Instead of recomputing the property from scratch for
every subarray (O(n²)), the window maintains the property incrementally as it slides,
giving O(n). The technique applies when: the problem asks about subarrays or
substrings, the property is monotone (adding elements can only increase or only
violate), and the answer involves an optimal contiguous segment. Source: MIT OCW
6.006 — Amortized Analysis.""",
    },
    {
        "id": "sliding_window_intuition",
        "pattern": "sliding_window",
        "topic": "intuition",
        "text": """Think of it as a rubber band stretched across an array. The right end can only
move right (expand the window). The left end moves right only when the window
violates the constraint. The rubber band snaps to the tightest valid configuration.
For 'longest substring without repeating characters': expand right until you see a
duplicate, then shrink left until the duplicate is gone, tracking the maximum window
size throughout. The key realization: you never need to move the right pointer left
because any window ending earlier was already considered. Source: Stanford CS161
Lecture Notes — Sliding Window.""",
    },
    {
        "id": "sliding_window_mechanics",
        "pattern": "sliding_window",
        "topic": "mechanics",
        "text": """Two variants: fixed-size window (window size k given) and variable-size window
(find optimal size). Fixed: maintain a window of exactly k, slide one step at a time,
add rightmost and remove leftmost. Variable: expand right always; shrink left when
constraint violated. Track answer at each valid state. For character problems, use a
frequency hash map inside the window. Key condition for shrinking: when does the
window become invalid? That condition drives the left pointer. window_size - max_freq
<= k is the famous condition for 'longest repeating character replacement'. Source:
CLRS Chapter 17 — Amortized Analysis.""",
    },
    {
        "id": "sliding_window_pitfalls",
        "pattern": "sliding_window",
        "topic": "pitfalls",
        "text": """Common sliding window mistakes: (1) Moving the left pointer too far — it should
only move until the constraint is restored, not past that point. (2) Forgetting to
update the answer before or after shrinking — check when to record the maximum.
(3) Off-by-one errors in window size calculation: right - left + 1 for inclusive indices.
(4) Confusing when the window is valid vs invalid and inverting the shrink condition.
Draw the window on paper and trace through 3-4 elements before coding. Source:
Stanford CS161 Problem Sets.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 4: STACK
    # ══════════════════════════════════════════════════════════
    {
        "id": "stack_concept",
        "pattern": "stack",
        "topic": "concept",
        "text": """A stack is a LIFO (Last In First Out) data structure with O(1) push and pop.
In algorithm design, a stack is used when you need to defer processing until a future
condition is met — you push work onto the stack and pop it when the trigger arrives.
The monotonic stack variant maintains a stack where elements are always in sorted
order (monotonically increasing or decreasing), which allows O(n) solutions to
problems about 'next greater element' or 'largest rectangle' that would otherwise
require O(n²) nested loops. Source: CLRS Section 10.1 — Stacks and Queues.""",
    },
    {
        "id": "stack_intuition",
        "pattern": "stack",
        "topic": "intuition",
        "text": """Think of a stack of plates. You can only add to or remove from the top. Now
imagine you're tracking temperatures and you want to know: for each day, how many
days until a warmer day? You process days left to right, pushing indices onto a stack.
When today is warmer than the stack's top, you've found the answer for that day —
pop it and record the distance. The stack holds 'unanswered questions': indices of
days still waiting for their warmer day. A monotonic stack is just this pattern with the
constraint that the values must stay sorted. Source: MIT OCW 6.006 — Monotonic
Stack.""",
    },
    {
        "id": "stack_mechanics",
        "pattern": "stack",
        "topic": "mechanics",
        "text": """For parentheses problems: push opening brackets, pop and match on closing.
For monotonic stack (daily temperatures, largest rectangle): maintain stack of indices.
Decreasing monotonic stack: pop when current element is greater than stack top.
Increasing monotonic stack: pop when current element is less than stack top. The
popped element's 'answer' is determined by the element that caused the pop (next
greater/smaller) and the element below it on the stack (previous greater/smaller).
For histogram rectangle: pop when shorter bar found, calculate area using the
new top as left boundary. Source: Stanford CS161 — Stack-Based Algorithms.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 5: BINARY SEARCH
    # ══════════════════════════════════════════════════════════
    {
        "id": "binary_search_concept",
        "pattern": "binary_search",
        "topic": "concept",
        "text": """Binary search finds a target in a sorted space in O(log n) by eliminating half
the remaining search space at each step. The key insight: if you can determine which
half of the space cannot contain the answer, you can discard it. Binary search applies
not just to sorted arrays but to any monotone decision space — 'binary search on the
answer' applies when the answer is a value and you can check feasibility in O(n),
giving O(n log n) total. The invariant: the answer always lies within [lo, hi].
Source: CLRS Chapter 2.3 — Designing Algorithms.""",
    },
    {
        "id": "binary_search_intuition",
        "pattern": "binary_search",
        "topic": "intuition",
        "text": """Think of guessing a number from 1 to 1000. Guess 500. 'Too high' — eliminate
the top half. Guess 250. 'Too low' — eliminate the bottom half. You never need more
than 10 guesses (log₂ 1000 ≈ 10). Binary search on the answer works when the
problem has a threshold property: for some value X, all values below X fail and all
values above X succeed (or vice versa). For Koko Eating Bananas: can Koko eat all
bananas at speed k within h hours? For speeds below some threshold: no. Above: yes.
Binary search finds that threshold in O(log(max_speed)) checks. Source: MIT OCW
6.006 Lecture 6.""",
    },
    {
        "id": "binary_search_mechanics",
        "pattern": "binary_search",
        "topic": "mechanics",
        "text": """Template: lo=0, hi=n-1, while lo <= hi: mid = (lo+hi)//2. If target found:
return mid. If target < arr[mid]: hi = mid-1. Else: lo = mid+1. For rotated array:
one half is always sorted — check which half and binary search accordingly. For
binary search on answer: lo=min_possible, hi=max_possible, binary search on
feasibility check. For finding leftmost/rightmost occurrence: don't return on match,
continue narrowing. Common bug: integer overflow in mid — use lo + (hi-lo)//2 in
languages with overflow. Source: CLRS Section 2.3.1.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 6: LINKED LIST
    # ══════════════════════════════════════════════════════════
    {
        "id": "linked_list_concept",
        "pattern": "linked_list",
        "topic": "concept",
        "text": """A linked list is a sequence of nodes where each node stores a value and a pointer
to the next node. Unlike arrays, linked lists have O(1) insertion and deletion at
known positions but O(n) access by index. Most linked list interview problems are
solved with pointer manipulation — changing which node points to which. The two
key techniques are: (1) two pointers at different speeds (fast/slow) for cycle detection
and finding midpoints; (2) reversing a sublist by rewiring pointers in place.
Source: CLRS Section 10.2 — Linked Lists.""",
    },
    {
        "id": "linked_list_intuition",
        "pattern": "linked_list",
        "topic": "intuition",
        "text": """Think of a conga line. To reverse it, each person turns around and grabs the
shoulders of the person who was behind them. You need three variables: prev (who you
just processed), curr (who you're processing now), and next (who comes after, saved
before you sever the connection). Floyd's cycle detection: two runners on a circular
track. A slow runner and a fast runner will eventually meet if and only if the track is
circular. The fast pointer moves twice as fast — if there's a cycle, they must meet inside
it. Source: MIT OCW 6.006 — Linked List Algorithms.""",
    },
    {
        "id": "linked_list_mechanics",
        "pattern": "linked_list",
        "topic": "mechanics",
        "text": """Reversal: prev=None, curr=head. While curr: next=curr.next, curr.next=prev,
prev=curr, curr=next. Return prev. Two-pointer (remove nth from end): place fast n
steps ahead, move both until fast hits end, slow is at the node before the target.
Cycle detection (Floyd): fast=slow=head, advance fast by 2 and slow by 1 each step,
they meet if cycle exists. Merge sorted lists: use a dummy head node to avoid special
casing the first node, always compare and attach the smaller node. Dummy head nodes
eliminate edge cases at list boundaries. Source: CLRS Exercise 10.2.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 7: TREES
    # ══════════════════════════════════════════════════════════
    {
        "id": "trees_concept",
        "pattern": "trees",
        "topic": "concept",
        "text": """A binary tree is a hierarchical structure where each node has at most two children.
Tree problems almost always use recursion because the tree structure itself is
recursive — a tree is a root node plus two subtrees. The key insight for most tree
problems: define what information you need to return from each subtree, then combine
those values at the current node. DFS (depth-first search) explores one path to a leaf
before backtracking; BFS (breadth-first search) explores all nodes at depth d before
depth d+1. Choose DFS for path problems, BFS for level-order problems.
Source: CLRS Chapter 12 — Binary Search Trees.""",
    },
    {
        "id": "trees_intuition",
        "pattern": "trees",
        "topic": "intuition",
        "text": """Think of the tree as a delegation chain. The root asks: 'what's the answer for
my left subtree? What's the answer for my right subtree? Given those answers, what's
my own answer?' This is the recursive tree pattern. For maximum path sum: each
node asks its children 'what's the best gain I can get from you?' and combines the
answers. The global maximum is tracked separately because the best path might pass
through a node without going up to its parent. For diameter: the diameter through any
node is left_height + right_height. Postorder traversal (process children before parent)
is the natural fit for bottom-up aggregation. Source: MIT OCW 6.006 Lecture 19.""",
    },
    {
        "id": "trees_mechanics",
        "pattern": "trees",
        "topic": "mechanics",
        "text": """DFS preorder (root-left-right): serialization, path problems. Inorder (left-root-right):
BST traversal gives sorted order. Postorder (left-right-root): height, diameter, deletion.
BFS: use a queue, process level by level. For BST validation: pass min/max bounds
through recursion, not just parent value. For LCA: if root is between p and q values
(BST), root is LCA. If both left, recurse left. If both right, recurse right. For construct
from preorder+inorder: preorder[0] is root, find it in inorder to split left and right
subtrees. Source: CLRS Section 12.1.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 8: TRIES
    # ══════════════════════════════════════════════════════════
    {
        "id": "tries_concept",
        "pattern": "tries",
        "topic": "concept",
        "text": """A trie (prefix tree) is a tree where each path from root to a node spells out a
prefix. Each node has up to 26 children (one per letter) and an is_end flag marking
complete words. Tries enable O(L) insertion, search, and prefix search where L is
the word length — independent of the number of stored words. Hash maps give O(L)
for exact lookup but O(n·L) for prefix queries (must scan all words). Tries trade space
(O(n·L) nodes) for fast prefix operations. Source: CLRS Problem 12-1 — Persistent
Data Structures.""",
    },
    {
        "id": "tries_intuition",
        "pattern": "tries",
        "topic": "intuition",
        "text": """Think of a trie as a filing cabinet organized by letter. All words starting with 'a'
share the same first drawer. All words starting with 'ap' share the same sub-drawer.
You don't need to check every word — you navigate the cabinet following the prefix's
path. If the path doesn't exist, no words have that prefix. If the path exists and ends
at an is_end node, the word exists. Word Search II uses a trie to search for multiple
words simultaneously across a grid — instead of running DFS for each word separately
(O(words × cells)), one DFS checks all words at once by following the trie.
Source: MIT OCW 6.006 — String Algorithms.""",
    },
    {
        "id": "tries_mechanics",
        "pattern": "tries",
        "topic": "mechanics",
        "text": """TrieNode: children = {} (or array of 26), is_end = False. Insert: for each char,
if char not in children create new node, move to children[char], set is_end=True at
end. Search: navigate, return False if any char missing, return is_end at last char.
StartsWith: same as search but return True regardless of is_end. For wildcard search
('.'): at a dot, recurse into all children. For Word Search II: build trie from word list,
run DFS on grid, move through trie and grid simultaneously, add word to results when
is_end reached. Mark visited cells during DFS. Source: Stanford CS161 — Trie
Data Structure.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 9: HEAP / PRIORITY QUEUE
    # ══════════════════════════════════════════════════════════
    {
        "id": "heap_concept",
        "pattern": "heap_priority_queue",
        "topic": "concept",
        "text": """A heap is a complete binary tree satisfying the heap property: every parent is
smaller (min-heap) or larger (max-heap) than its children. It supports O(log n) push
and pop while maintaining the min/max at the root in O(1). Use a heap when you
repeatedly need the minimum or maximum from a dynamic collection. Python's heapq
is a min-heap; negate values for max-heap behavior. Heaps are the right data structure
for: k-way merging, finding the kth largest/smallest, streaming medians, and task
scheduling. Source: CLRS Chapter 6 — Heapsort.""",
    },
    {
        "id": "heap_intuition",
        "pattern": "heap_priority_queue",
        "topic": "intuition",
        "text": """Think of a heap as a priority line at a hospital emergency room. The most critical
patient (highest priority = min value for min-heap) always gets served first, regardless
of when they arrived. For 'find median from data stream': maintain two heaps — a
max-heap for the lower half and a min-heap for the upper half. Balance them so they
differ by at most one element. The median is either the top of the larger heap or the
average of both tops. This gives O(log n) insertion and O(1) median — much better
than sorting every time. Source: MIT OCW 6.006 — Priority Queues.""",
    },
    {
        "id": "heap_mechanics",
        "pattern": "heap_priority_queue",
        "topic": "mechanics",
        "text": """K largest elements: maintain a min-heap of size k. For each element, push it;
if size > k, pop (evicts the smallest, keeping k largest). K closest points: same
pattern with max-heap on distance. Merge k sorted lists: push (value, list_index,
element_index) for each list's first element; repeatedly pop min and push the next
element from that list. Task scheduler: count frequencies, use max-heap of (negative
count, task), simulate cooldown with a queue. For two-heap median: push to max-heap,
rebalance by moving tops between heaps to maintain size property.
Source: CLRS Exercise 6.5.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 10: BACKTRACKING
    # ══════════════════════════════════════════════════════════
    {
        "id": "backtracking_concept",
        "pattern": "backtracking",
        "topic": "concept",
        "text": """Backtracking is a systematic method for exploring all possible solutions by building
candidates incrementally and abandoning (backtracking from) partial candidates as
soon as it's determined they cannot lead to a valid solution. It is DFS on an implicit
decision tree. At each node, you choose from available options; if a choice leads to
a dead end, you undo it (backtrack) and try the next option. Backtracking applies when:
you need all solutions (subsets, permutations, combinations), the search space is
exponential but can be pruned. Source: CLRS Chapter 35 — NP-Completeness.""",
    },
    {
        "id": "backtracking_intuition",
        "pattern": "backtracking",
        "topic": "intuition",
        "text": """Think of solving a maze. At each junction, you pick a direction. If you hit a dead
end, you trace back to the last junction and try another direction. You never re-explore
a path you've already exhausted. For subsets: at each element, you make a binary
choice — include it or exclude it. For permutations: at each position, try each unused
element. The call stack is your 'memory' of decisions made so far. The critical operation
is the undo step: whatever you add to the current path before the recursive call, you
remove after. The path variable must be in the same state when the recursive call
returns as it was when it was made. Source: MIT OCW 6.046 — Backtracking.""",
    },
    {
        "id": "backtracking_mechanics",
        "pattern": "backtracking",
        "topic": "mechanics",
        "text": """Template: def backtrack(start, current_path): if valid complete state: results.append.
For each choice from start to end: if pruning condition: continue. make choice (append
to path). recurse(next_start, current_path). undo choice (pop from path). For subsets:
recurse with start+1 to avoid reuse (or start for combinations). For permutations:
use a 'used' boolean array. For duplicates (Subsets II): sort first, skip duplicate
elements at the same recursion level with 'if i > start and nums[i] == nums[i-1]:
continue'. Source: Stanford CS161 — Combinatorial Search.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 11: GRAPHS
    # ══════════════════════════════════════════════════════════
    {
        "id": "graphs_concept",
        "pattern": "graphs",
        "topic": "concept",
        "text": """A graph is a set of vertices connected by edges. Graph problems model
relationships: islands in a grid, dependencies between tasks, network connections.
DFS explores as deep as possible before backtracking; BFS explores level by level.
BFS guarantees shortest path in unweighted graphs because it explores all paths of
length k before any path of length k+1. Use a 'visited' set to prevent re-processing.
Graph problems on grids: treat each cell as a node, its unvisited neighbors as edges.
Source: CLRS Chapter 22 — Elementary Graph Algorithms.""",
    },
    {
        "id": "graphs_intuition",
        "pattern": "graphs",
        "topic": "intuition",
        "text": """Think of graph DFS as exploring a cave system. You pick a tunnel and follow it
all the way until you hit a dead end or a place you've been before, then backtrack
and try another tunnel. BFS is like a ripple expanding from a stone dropped in water
— all cells at distance 1 are explored before any cell at distance 2. For number of
islands: DFS from each unvisited '1' cell, marking all connected land cells as visited.
Each time you start a new DFS from an unvisited '1', you've found a new island.
Source: MIT OCW 6.006 Lecture 13 — Graph Search.""",
    },
    {
        "id": "graphs_mechanics",
        "pattern": "graphs",
        "topic": "mechanics",
        "text": """DFS template: def dfs(node, visited): visited.add(node). for neighbor in
graph[node]: if neighbor not in visited: dfs(neighbor, visited). BFS template: queue
= deque([start]), visited = {start}. While queue: node = popleft(). For neighbor:
if not visited: visited.add, queue.append. Grid DFS: directions = [(0,1),(0,-1),(1,0),
(-1,0)]. Check bounds and visited before recursing. For clone graph: map old→new
nodes in a hash map, DFS building the clone. Cycle detection in directed graph:
maintain recursion stack (gray nodes) separate from visited (black nodes).
Source: CLRS Section 22.3 — Depth-First Search.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 12: DYNAMIC PROGRAMMING 1D
    # ══════════════════════════════════════════════════════════
    {
        "id": "dp_1d_concept",
        "pattern": "dynamic_programming_1d",
        "topic": "concept",
        "text": """Dynamic programming solves problems with overlapping subproblems and optimal
substructure by storing subproblem solutions to avoid recomputation. 1D DP uses an
array dp[] where dp[i] represents the optimal solution for the subproblem ending at
or considering only elements up to index i. The recurrence relation defines how dp[i]
depends on dp[i-1], dp[i-2], etc. Memoization (top-down) stores recursive results;
tabulation (bottom-up) builds the table iteratively. Both give the same asymptotic
complexity. Source: CLRS Chapter 15 — Dynamic Programming.""",
    },
    {
        "id": "dp_1d_intuition",
        "pattern": "dynamic_programming_1d",
        "topic": "intuition",
        "text": """Think of DP as committing to memory: instead of recomputing the same
subproblem ten times, you write down the answer the first time and look it up
thereafter. For climbing stairs: you can reach step n from step n-1 or n-2. So the
number of ways to reach step n equals the number of ways to reach n-1 plus n-2.
This is Fibonacci — but DP makes it O(n) instead of exponential. The key question
for any DP problem: 'If I knew the optimal solution for all smaller subproblems, how
would I compute the optimal solution for this subproblem?' That question defines the
recurrence. Source: MIT OCW 6.006 Lecture 19 — Dynamic Programming.""",
    },
    {
        "id": "dp_1d_mechanics",
        "pattern": "dynamic_programming_1d",
        "topic": "mechanics",
        "text": """Coin change: dp[i] = min coins to make amount i = min(dp[i-coin] + 1) for all
coins. LIS: dp[i] = longest increasing subsequence ending at i = max(dp[j]+1) for
j < i where nums[j] < nums[i]. House Robber: dp[i] = max(dp[i-1], dp[i-2]+nums[i]).
Word Break: dp[i] = True if any dp[j] is True and s[j:i] is in word_dict. Decode Ways:
dp[i] += dp[i-1] if single digit valid; dp[i] += dp[i-2] if two-digit valid. Space
optimization: when dp[i] only depends on dp[i-1] and dp[i-2], you can use two
variables instead of the full array. Source: CLRS Section 15.1.""",
    },
    {
        "id": "dp_1d_pitfalls",
        "pattern": "dynamic_programming_1d",
        "topic": "pitfalls",
        "text": """Common 1D DP mistakes: (1) Wrong base case — dp[0] must be initialized correctly
(usually 0 or 1 depending on the problem). (2) Wrong recurrence direction — make
sure you're building up from smaller subproblems. (3) Off-by-one errors — does dp[i]
represent 'using the first i elements' or 'ending at index i'? Be explicit. (4) Forgetting
that some problems require the full dp array (for reconstruction) while others can
be space-optimized to O(1). (5) For problems like House Robber II (circular array),
run the 1D DP twice (skip first element, skip last) and take the max.
Source: CLRS Exercise 15.1.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 13: DYNAMIC PROGRAMMING 2D
    # ══════════════════════════════════════════════════════════
    {
        "id": "dp_2d_concept",
        "pattern": "dynamic_programming_2d",
        "topic": "concept",
        "text": """2D DP uses a matrix dp[i][j] where the two indices represent two sequences,
dimensions, or decision axes. Most 2D DP problems involve comparing two strings or
filling a grid. Longest Common Subsequence: dp[i][j] = LCS of first i chars of s1
and first j chars of s2. Edit Distance: dp[i][j] = min operations to convert s1[:i]
to s2[:j]. Unique Paths: dp[i][j] = paths to cell (i,j). The recurrence connects
dp[i][j] to dp[i-1][j], dp[i][j-1], and dp[i-1][j-1]. Source: CLRS Section
15.4 — Longest Common Subsequence.""",
    },
    {
        "id": "dp_2d_intuition",
        "pattern": "dynamic_programming_2d",
        "topic": "intuition",
        "text": """Think of 2D DP as filling a grid where each cell's answer depends on its
neighbors to the left, above, and diagonally above-left. For LCS: if the current
characters match, extend the diagonal (dp[i-1][j-1] + 1). If they don't match,
take the better of skipping from either string (max of dp[i-1][j], dp[i][j-1]).
For edit distance: if characters match, no operation needed (copy diagonal). If they
differ, take the minimum of insert (left+1), delete (above+1), replace (diagonal+1).
Visualize the grid being filled row by row, left to right. Source: MIT OCW 6.006
Lecture 20 — DP on Sequences.""",
    },
    {
        "id": "dp_2d_mechanics",
        "pattern": "dynamic_programming_2d",
        "topic": "mechanics",
        "text": """LCS: dp = (m+1)×(n+1) zeros. For i,j: if s1[i-1]==s2[j-1]: dp[i][j]=dp[i-1][j-1]+1
else: dp[i][j]=max(dp[i-1][j], dp[i][j-1]). Answer: dp[m][n]. Edit Distance: same
grid, if chars match: dp[i-1][j-1], else: 1+min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]).
Unique Paths: dp[i][j]=dp[i-1][j]+dp[i][j-1], top row and left column all 1s. Space
optimization: LCS and edit distance can be reduced to O(min(m,n)) space using two
rows. Regular Expression: handle '.' (match any) and '*' (zero or more of preceding)
separately in the recurrence. Source: CLRS Section 15.4.""",
    },

    # ══════════════════════════════════════════════════════════
    # PATTERN 14: GREEDY
    # ══════════════════════════════════════════════════════════
    {
        "id": "greedy_concept",
        "pattern": "greedy",
        "topic": "concept",
        "text": """A greedy algorithm makes the locally optimal choice at each step with the hope
of reaching the global optimum. Unlike DP, greedy does not reconsider choices.
Greedy works when the problem has a 'greedy choice property' — a local optimal
choice leads to a globally optimal solution — and 'optimal substructure' — an
optimal solution contains optimal solutions to subproblems. Greedy is harder to
prove correct than DP but simpler to implement. Always ask: does making the best
local choice now ever prevent a better global solution? If not, greedy works.
Source: CLRS Chapter 16 — Greedy Algorithms.""",
    },
    {
        "id": "greedy_intuition",
        "pattern": "greedy",
        "topic": "intuition",
        "text": """Think of Jump Game: you're on a road with gas stations. At each station you can
refuel (jump forward by up to nums[i]). The greedy insight: at each position, track
the farthest you can possibly reach from any position you've already visited. If at
any position your farthest reachable is less than your current position, you're stuck.
You don't need to know the optimal sequence of jumps — you just need to know
whether the farthest reachable frontier ever advances past the end. This local decision
(track max reach) gives the global answer (can you reach the end). Source: MIT OCW
6.046 — Greedy Algorithms.""",
    },
    {
        "id": "greedy_mechanics",
        "pattern": "greedy",
        "topic": "mechanics",
        "text": """Jump Game: max_reach = 0; for i, v in enumerate(nums): if i > max_reach: return
False; max_reach = max(max_reach, i+v). Jump Game II: track current jump's farthest
and next jump's farthest, increment jumps when you reach current boundary. Gas
Station: track total_gain and current_gain; if current_gain < 0, reset start to next
station. Merge Intervals: sort by start, merge if current start <= previous end, update
end to max. Meeting Rooms II: sort by start, use min-heap of end times, pop if earliest
end <= current start (reuse room), else push new room. Source: CLRS Section 16.2.""",
    },
    {
        "id": "greedy_pitfalls",
        "pattern": "greedy",
        "topic": "pitfalls",
        "text": """Common greedy mistakes: (1) Applying greedy to a DP problem — the local optimum
doesn't lead to global optimum. Test: can a greedy choice now block a better
future choice? (2) Forgetting to sort before greedy — most interval and scheduling
problems require sorting first. (3) Confusing 'earliest deadline first' with 'shortest
job first' — the correct greedy criterion depends on the optimization objective.
(4) For coin change: greedy (always pick largest coin) only works for canonical coin
systems (like US currency). For arbitrary denominations, use DP. Source: CLRS
Section 16.1 — An Activity-Selection Problem.""",
    },

    # ══════════════════════════════════════════════════════════
    # CROSS-PATTERN: PROBLEM RECOGNITION
    # ══════════════════════════════════════════════════════════
    {
        "id": "pattern_recognition",
        "pattern": "general",
        "topic": "recognition",
        "text": """How to identify which pattern a problem uses: Arrays/Hashing — pairs, complements,
duplicates, frequency count, O(n²) brute force reducible to O(n). Two Pointers —
sorted array, pairs summing to target, palindrome, partition. Sliding Window —
contiguous subarray/substring, optimal length, constraint on window contents.
Stack — matching brackets, next greater element, monotonic sequences, histogram.
Binary Search — sorted input, find threshold, feasibility check. Linked List — in-place
modification, cycle, kth element from end. Trees — hierarchical data, recursion
natural. Tries — prefix operations, multiple string lookup. Heap — kth element,
streaming data, k-way merge. Backtracking — enumerate all solutions, exponential
search space with pruning. Graphs — relationships, connectivity, shortest path.
DP — overlapping subproblems, optimization, count of ways. Greedy — interval
scheduling, optimization with local choice property. Source: AlgoSensei Knowledge Base.""",
    },
]

def get_chunks_by_pattern(pattern: str) -> list[dict]:
    return [c for c in KNOWLEDGE_BASE if c["pattern"] == pattern]

def get_all_chunks() -> list[dict]:
    return KNOWLEDGE_BASE

def get_patterns() -> list[str]:
    return sorted(set(c["pattern"] for c in KNOWLEDGE_BASE))
