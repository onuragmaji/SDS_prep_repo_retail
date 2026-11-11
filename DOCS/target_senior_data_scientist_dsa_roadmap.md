# Senior Data Scientist -- DSA Practice Roadmap

A practical LeetCode checklist for preparing for Data Scientist coding
assessments, including the patterns exposed by the recent Target
HackerEarth assessment.

**Goal:** Build reliable problem-solving and pattern-recognition skills
without preparing as if this were a full-time Software Engineering
competitive-programming interview.

**How to use this roadmap** - Work through the sections in priority
order. - Try each problem yourself before looking at solutions. - For
each problem, write down: input, required output, constraints, key
observation, algorithm, and time/space complexity. - Aim to solve Easy
problems confidently and a good range of Medium problems
independently. - The Target questions listed at the end are recalled
examples from the assessment, not a guarantee of future questions.

------------------------------------------------------------------------

## Priority overview

  ------------------------------------------------------------------------
  Priority              Areas                             Suggested effort
  --------------------- --------------------- ----------------------------
  P1 -- Core            Arrays, strings,                               40%
                        hashing, sorting,     
                        binary search, two    
                        pointers, sliding     
                        window, prefix sums   

  P2 -- Important       BFS, DFS, queues,                              40%
  additions             stacks, matrices,     
                        GCD, primes,          
                        mathematical          
                        counting, greedy      

  P3 -- Familiarity     Trees, heaps,                                  20%
                        recursion, basic      
                        dynamic programming,  
                        graph shortest paths  
  ------------------------------------------------------------------------

------------------------------------------------------------------------

# Section 1 -- Arrays and Strings

**Priority: P1 -- Core**

### Concepts to know

-   Array traversal and indexing
-   Finding minimum/maximum
-   In-place updates
-   Frequency and duplicate detection
-   Subarrays versus subsequences
-   String traversal and character counting

### LeetCode practice

1.  [Two Sum -- 1](https://leetcode.com/problems/two-sum/)
2.  [Best Time to Buy and Sell Stock --
    121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
3.  [Contains Duplicate --
    217](https://leetcode.com/problems/contains-duplicate/)
4.  [Product of Array Except Self --
    238](https://leetcode.com/problems/product-of-array-except-self/)
5.  [Maximum Subarray --
    53](https://leetcode.com/problems/maximum-subarray/)
6.  [Move Zeroes -- 283](https://leetcode.com/problems/move-zeroes/)
7.  [Valid Anagram -- 242](https://leetcode.com/problems/valid-anagram/)
8.  [Longest Common Prefix --
    14](https://leetcode.com/problems/longest-common-prefix/)

**Be comfortable with:** loops, indexing, sets, dictionaries, and
handling empty or single-element inputs.

------------------------------------------------------------------------

# Section 2 -- Hashing and Frequency Counting

**Priority: P1 -- Core**

### Concepts to know

-   Python dictionaries and sets
-   Frequency maps
-   Counting pairs
-   Grouping items by a derived key
-   Prefix-sum frequency maps
-   Avoiding repeated nested-loop comparisons

### LeetCode practice

1.  [Two Sum -- 1](https://leetcode.com/problems/two-sum/)
2.  [Valid Anagram -- 242](https://leetcode.com/problems/valid-anagram/)
3.  [Group Anagrams --
    49](https://leetcode.com/problems/group-anagrams/)
4.  [Majority Element --
    169](https://leetcode.com/problems/majority-element/)
5.  [Top K Frequent Elements --
    347](https://leetcode.com/problems/top-k-frequent-elements/)
6.  [Number of Good Pairs --
    1512](https://leetcode.com/problems/number-of-good-pairs/)
7.  [Number of Pairs of Interchangeable Rectangles --
    2001](https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/)
8.  [Subarray Sum Equals K --
    560](https://leetcode.com/problems/subarray-sum-equals-k/)

**Key pattern:** If a question asks how many items or pairs satisfy a
condition, check whether a dictionary can store counts or group items by
a normalised key.

------------------------------------------------------------------------

# Section 3 -- Two Pointers

**Priority: P1 -- Core**

### Concepts to know

-   Left and right pointers
-   Moving pointers based on a condition
-   Sorted-array pair problems
-   In-place array modification
-   Removing duplicates

### LeetCode practice

1.  [Valid Palindrome --
    125](https://leetcode.com/problems/valid-palindrome/)
2.  [Two Sum II -- Input Array Is Sorted --
    167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)
3.  [Remove Duplicates from Sorted Array --
    26](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)
4.  [Move Zeroes -- 283](https://leetcode.com/problems/move-zeroes/)
5.  [Container With Most Water --
    11](https://leetcode.com/problems/container-with-most-water/)
6.  [3Sum -- 15](https://leetcode.com/problems/3sum/)

------------------------------------------------------------------------

# Section 4 -- Sliding Window

**Priority: P1 -- Core**

### Concepts to know

-   Fixed-size window
-   Variable-size window
-   Expanding and shrinking a window
-   Maintaining counts while moving the window
-   Recognising contiguous subarray/substring questions

### LeetCode practice

1.  [Maximum Average Subarray I --
    643](https://leetcode.com/problems/maximum-average-subarray-i/)
2.  [Best Time to Buy and Sell Stock --
    121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
3.  [Longest Substring Without Repeating Characters --
    3](https://leetcode.com/problems/longest-substring-without-repeating-characters/)
4.  [Minimum Size Subarray Sum --
    209](https://leetcode.com/problems/minimum-size-subarray-sum/)
5.  [Permutation in String --
    567](https://leetcode.com/problems/permutation-in-string/)
6.  [Longest Repeating Character Replacement --
    424](https://leetcode.com/problems/longest-repeating-character-replacement/)

------------------------------------------------------------------------

# Section 5 -- Prefix Sums and Kadane's Algorithm

**Priority: P1 -- Core**

### Concepts to know

-   Running sum
-   Prefix sum arrays
-   Range-sum queries
-   Prefix sum combined with hashing
-   Maximum subarray sum (Kadane's algorithm)
-   Prefix and suffix products

### LeetCode practice

1.  [Running Sum of 1d Array --
    1480](https://leetcode.com/problems/running-sum-of-1d-array/)
2.  [Range Sum Query -- Immutable --
    303](https://leetcode.com/problems/range-sum-query-immutable/)
3.  [Maximum Subarray --
    53](https://leetcode.com/problems/maximum-subarray/)
4.  [Subarray Sum Equals K --
    560](https://leetcode.com/problems/subarray-sum-equals-k/)
5.  [Product of Array Except Self --
    238](https://leetcode.com/problems/product-of-array-except-self/)
6.  [Maximum Sum Circular Subarray --
    918](https://leetcode.com/problems/maximum-sum-circular-subarray/)

------------------------------------------------------------------------

# Section 6 -- Sorting and Intervals

**Priority: P1 -- Core**

### Concepts to know

-   Python `sorted()` and `.sort()`
-   Custom sort keys
-   Sorting pairs/tuples
-   Sorting before using two pointers
-   Interval merging and overlap detection

### LeetCode practice

1.  [Merge Sorted Array --
    88](https://leetcode.com/problems/merge-sorted-array/)
2.  [Merge Intervals --
    56](https://leetcode.com/problems/merge-intervals/)
3.  [Meeting Rooms -- 252](https://leetcode.com/problems/meeting-rooms/)
4.  [Non-overlapping Intervals --
    435](https://leetcode.com/problems/non-overlapping-intervals/)
5.  [Sort Colors -- 75](https://leetcode.com/problems/sort-colors/)

------------------------------------------------------------------------

# Section 7 -- Binary Search

**Priority: P1 -- Core**

### Concepts to know

-   Standard binary search
-   Search insertion position
-   First/last occurrence
-   Search on a condition (binary search on answer)
-   Avoiding off-by-one errors
-   Understanding loop conditions and boundaries

### LeetCode practice

1.  [Binary Search -- 704](https://leetcode.com/problems/binary-search/)
2.  [Search Insert Position --
    35](https://leetcode.com/problems/search-insert-position/)
3.  [First Bad Version --
    278](https://leetcode.com/problems/first-bad-version/)
4.  [Find First and Last Position of Element in Sorted Array --
    34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
5.  [Search in Rotated Sorted Array --
    33](https://leetcode.com/problems/search-in-rotated-sorted-array/)
6.  [Koko Eating Bananas --
    875](https://leetcode.com/problems/koko-eating-bananas/)

------------------------------------------------------------------------

# Section 8 -- Stack and Queue

**Priority: P2 -- Important**

### Concepts to know

-   Stack: last in, first out
-   Queue: first in, first out
-   Python list as a stack
-   `collections.deque` as a queue
-   Monotonic stack basics
-   When a queue is needed for BFS

### LeetCode practice

1.  [Valid Parentheses --
    20](https://leetcode.com/problems/valid-parentheses/)
2.  [Implement Queue using Stacks --
    232](https://leetcode.com/problems/implement-queue-using-stacks/)
3.  [Implement Stack using Queues --
    225](https://leetcode.com/problems/implement-stack-using-queues/)
4.  [Daily Temperatures --
    739](https://leetcode.com/problems/daily-temperatures/)
5.  [Evaluate Reverse Polish Notation --
    150](https://leetcode.com/problems/evaluate-reverse-polish-notation/)
6.  [Number of Recent Calls --
    933](https://leetcode.com/problems/number-of-recent-calls/)

**Python reminder:**

``` python
from collections import deque

queue = deque()
queue.append(value)
first = queue.popleft()
```

------------------------------------------------------------------------

# Section 9 -- BFS and Graph Traversal

**Priority: P2 -- Important; especially relevant to the recent
assessment**

### Concepts to know

-   Graphs represented using adjacency lists
-   BFS using a queue
-   Visited sets/arrays
-   Level-by-level traversal
-   Multi-source BFS
-   Shortest path in an unweighted graph
-   Grid movement: up, down, left, right
-   Converting an array problem into a graph problem

### LeetCode practice

1.  [Rotting Oranges --
    994](https://leetcode.com/problems/rotting-oranges/)
2.  [Number of Islands --
    200](https://leetcode.com/problems/number-of-islands/)
3.  [Shortest Path in Binary Matrix --
    1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/)
4.  [01 Matrix -- 542](https://leetcode.com/problems/01-matrix/)
5.  [Binary Tree Level Order Traversal --
    102](https://leetcode.com/problems/binary-tree-level-order-traversal/)
6.  [Open the Lock -- 752](https://leetcode.com/problems/open-the-lock/)

### BFS template to understand

``` python
from collections import deque

queue = deque([start])
visited = {start}

while queue:
    node = queue.popleft()

    for neighbour in get_neighbours(node):
        if neighbour not in visited:
            visited.add(neighbour)
            queue.append(neighbour)
```

**Important:** In shortest-path or minimum-time problems with equal-cost
moves, BFS is often a strong candidate. For simultaneous spread from
multiple starting points, initialise the queue with all starting points
(multi-source BFS).

------------------------------------------------------------------------

# Section 10 -- DFS and Connected Components

**Priority: P2 -- Important**

### Concepts to know

-   Recursive DFS
-   Iterative DFS using a stack
-   Visited tracking
-   Connected components
-   Flood fill
-   Grid traversal

### LeetCode practice

1.  [Max Area of Island --
    695](https://leetcode.com/problems/max-area-of-island/)
2.  [Number of Islands --
    200](https://leetcode.com/problems/number-of-islands/)
3.  [Flood Fill -- 733](https://leetcode.com/problems/flood-fill/)
4.  [Find if Path Exists in Graph --
    1971](https://leetcode.com/problems/find-if-path-exists-in-graph/)
5.  [Keys and Rooms --
    841](https://leetcode.com/problems/keys-and-rooms/)

------------------------------------------------------------------------

# Section 11 -- Matrix and Grid Problems

**Priority: P2 -- Important**

### Concepts to know

-   Row and column traversal
-   Four-directional and eight-directional neighbours
-   Boundary checks
-   In-place marking versus a visited matrix
-   BFS/DFS on grids

### LeetCode practice

1.  [Flood Fill -- 733](https://leetcode.com/problems/flood-fill/)
2.  [Rotting Oranges --
    994](https://leetcode.com/problems/rotting-oranges/)
3.  [Number of Islands --
    200](https://leetcode.com/problems/number-of-islands/)
4.  [Island Perimeter --
    463](https://leetcode.com/problems/island-perimeter/)
5.  [Spiral Matrix -- 54](https://leetcode.com/problems/spiral-matrix/)
6.  [Set Matrix Zeroes --
    73](https://leetcode.com/problems/set-matrix-zeroes/)

------------------------------------------------------------------------

# Section 12 -- Mathematics and Number Theory

**Priority: P2 -- Important; a key gap exposed by the assessment**

### Concepts to know

-   Prime number checking
-   Efficient prime checking up to square root of `n`
-   Sieve of Eratosthenes
-   GCD and LCM
-   Prime factorisation
-   Divisibility and common factors
-   Ratio normalisation
-   Modular arithmetic basics
-   Integer division and remainder
-   Combinations and pair counting

### LeetCode practice

1.  [Count Primes -- 204](https://leetcode.com/problems/count-primes/)
2.  [Find Greatest Common Divisor of Array --
    1979](https://leetcode.com/problems/find-greatest-common-divisor-of-array/)
3.  [Number of Pairs of Interchangeable Rectangles --
    2001](https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/)
4.  [Number of Good Pairs --
    1512](https://leetcode.com/problems/number-of-good-pairs/)
5.  [Ugly Number -- 263](https://leetcode.com/problems/ugly-number/)
6.  [Check if It Is a Straight Line --
    1232](https://leetcode.com/problems/check-if-it-is-a-straight-line/)
7.  [Minimum Jumps to Reach End via Prime Teleportation --
    3629](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/)

### Python techniques

``` python
import math

# GCD
g = math.gcd(a, b)

# LCM (Python 3.9+)
l = math.lcm(a, b)

# Prime check
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True

# Number of pairs from a group of n equal items
pairs = n * (n - 1) // 2
```

### Sieve of Eratosthenes

Understand how to generate all primes up to `n` efficiently, rather than
checking every number independently.

------------------------------------------------------------------------

# Section 13 -- Greedy Algorithms and Jump Problems

**Priority: P2 -- Important**

### Concepts to know

-   Making locally optimal choices
-   Tracking the farthest reachable index
-   Minimum jumps
-   Sorting followed by greedy selection
-   Recognising when greedy is valid versus when BFS/DP is needed

### LeetCode practice

1.  [Jump Game -- 55](https://leetcode.com/problems/jump-game/)
2.  [Jump Game II -- 45](https://leetcode.com/problems/jump-game-ii/)
3.  [Gas Station -- 134](https://leetcode.com/problems/gas-station/)
4.  [Assign Cookies --
    455](https://leetcode.com/problems/assign-cookies/)
5.  [Non-overlapping Intervals --
    435](https://leetcode.com/problems/non-overlapping-intervals/)

------------------------------------------------------------------------

# Section 14 -- Recursion and Backtracking

**Priority: P3 -- Familiarity**

### Concepts to know

-   Base case and recursive case
-   Call stack
-   Generating combinations and subsets
-   Basic backtracking
-   Avoiding repeated states

### LeetCode practice

1.  [Fibonacci Number --
    509](https://leetcode.com/problems/fibonacci-number/)
2.  [Subsets -- 78](https://leetcode.com/problems/subsets/)
3.  [Permutations -- 46](https://leetcode.com/problems/permutations/)
4.  [Combination Sum --
    39](https://leetcode.com/problems/combination-sum/)

------------------------------------------------------------------------

# Section 15 -- Trees and Heaps

**Priority: P3 -- Familiarity**

### Concepts to know

-   Binary tree structure
-   Preorder, inorder and postorder traversal
-   Level-order traversal
-   Basic BST search
-   Min-heap and max-heap
-   Python `heapq`
-   Top K elements

### LeetCode practice

1.  [Maximum Depth of Binary Tree --
    104](https://leetcode.com/problems/maximum-depth-of-binary-tree/)
2.  [Invert Binary Tree --
    226](https://leetcode.com/problems/invert-binary-tree/)
3.  [Binary Tree Level Order Traversal --
    102](https://leetcode.com/problems/binary-tree-level-order-traversal/)
4.  [Validate Binary Search Tree --
    98](https://leetcode.com/problems/validate-binary-search-tree/)
5.  [Kth Largest Element in an Array --
    215](https://leetcode.com/problems/kth-largest-element-in-an-array/)
6.  [Top K Frequent Elements --
    347](https://leetcode.com/problems/top-k-frequent-elements/)

------------------------------------------------------------------------

# Section 16 -- Basic Dynamic Programming

**Priority: P3 -- Familiarity**

### Concepts to know

-   Recognising overlapping subproblems
-   Memoisation versus tabulation
-   One-dimensional DP
-   State definition and transition
-   Basic space optimisation

### LeetCode practice

1.  [Climbing Stairs --
    70](https://leetcode.com/problems/climbing-stairs/)
2.  [Min Cost Climbing Stairs --
    746](https://leetcode.com/problems/min-cost-climbing-stairs/)
3.  [House Robber -- 198](https://leetcode.com/problems/house-robber/)
4.  [Maximum Subarray --
    53](https://leetcode.com/problems/maximum-subarray/)
5.  [Coin Change -- 322](https://leetcode.com/problems/coin-change/)

------------------------------------------------------------------------

# Section 17 -- Mixed Problem-Solving and Assessment Practice

**Priority: P2 -- Important**

Practise problems without looking at their topic labels first. The
purpose is to identify the pattern from the statement.

Suggested mixed set: 1. [Minimum Jumps to Reach End via Prime
Teleportation --
3629](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/)
2. [Number of Pairs of Interchangeable Rectangles --
2001](https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/)
3. [Rotting Oranges --
994](https://leetcode.com/problems/rotting-oranges/) 4. [Open the Lock
-- 752](https://leetcode.com/problems/open-the-lock/) 5. [Subarray Sum
Equals K -- 560](https://leetcode.com/problems/subarray-sum-equals-k/)
6. [Koko Eating Bananas --
875](https://leetcode.com/problems/koko-eating-bananas/) 7. [Jump Game
II -- 45](https://leetcode.com/problems/jump-game-ii/)

For each problem, practise explaining: 1. What is given? 2. What exactly
must be returned? 3. What are the movement or validity rules? 4. What is
the brute-force approach? 5. Which pattern improves it? 6. What is the
time and space complexity? 7. What edge cases could break the solution?

------------------------------------------------------------------------

# Appendix -- Questions recalled from the recent Target HackerEarth assessment

These are the three LeetCode problems identified as closely resembling
questions encountered in the assessment. The original assessment wording
and examples may have differed. Treat these as preparation references,
not confirmed verbatim copies.

## 1. Minimum Jumps to Reach End via Prime Teleportation

**LeetCode:** [3629 -- Minimum Jumps to Reach End via Prime
Teleportation](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/)

**Topics to prepare:** - Graph modelling - BFS and shortest path - Prime
numbers - Prime factorisation - Divisibility - Hash maps / grouping
indices - Visited tracking

**Why it matters:** An array movement problem can actually be a graph
shortest-path problem when special jumps connect otherwise distant
positions.

## 2. Number of Pairs of Interchangeable Rectangles

**LeetCode:** [2001 -- Number of Pairs of Interchangeable
Rectangles](https://leetcode.com/problems/number-of-pairs-of-interchangeable-rectangles/)

**Topics to prepare:** - GCD - Ratio simplification - Hash maps /
frequency counting - Combinations and pair counting - Integer arithmetic
and precision

**Why it matters:** Recognise that different width-height pairs can
represent the same ratio. Normalise the ratio, group equal ratios and
count pairs.

## 3. Rotting Oranges

**LeetCode:** [994 -- Rotting
Oranges](https://leetcode.com/problems/rotting-oranges/)

**Topics to prepare:** - BFS - Multi-source BFS - Queue
(`collections.deque`) - Matrix traversal - Four-directional neighbours -
Visited/state tracking - Level-by-level processing

**Why it matters:** When multiple starting points spread simultaneously
and the question asks for minimum time, consider multi-source BFS.

------------------------------------------------------------------------

## Final preparation checklist

Use this as a progress tracker.

### Core topics

-   [ ] Arrays and strings
-   [ ] Hashing and frequency counting
-   [ ] Two pointers
-   [ ] Sliding window
-   [ ] Prefix sums and Kadane's algorithm
-   [ ] Sorting and intervals
-   [ ] Binary search

### Additional topics highlighted by the assessment

-   [ ] Stack and queue
-   [ ] BFS
-   [ ] DFS
-   [ ] Matrix and grid traversal
-   [ ] Prime numbers and sieve
-   [ ] GCD, LCM and ratio simplification
-   [ ] Mathematical counting and combinations
-   [ ] Greedy and jump problems

### Further familiarity

-   [ ] Recursion and backtracking
-   [ ] Trees and heaps
-   [ ] Basic dynamic programming

**Final advice:** Do not try to complete every listed problem in one go.
Start with P1, then prioritise BFS, number theory and mathematical
counting from P2. The goal is to recognise unfamiliar problem patterns
and implement a correct, efficient solution under time pressure.
