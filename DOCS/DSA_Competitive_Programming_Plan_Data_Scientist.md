# Competitive Programming / DSA Preparation Plan for Data Scientist Interviews

## Objective

Target roles: Senior Data Scientist roles at retail/product companies such as Target, Walmart, H&M, and similar organizations.

The goal is **not** to become a competitive programmer.

The goal is to become sufficiently fast and reliable at common DSA patterns so that a coding/competitive-programming round does not become a blocker.

### Target outcome

By the end of this preparation, aim to:

- Solve common Easy problems in ~10–15 minutes.
- Solve common Medium problems in ~25–35 minutes.
- Recognize the underlying pattern quickly.
- Explain brute force → optimized approach → complexity clearly.
- Write clean Python without spending time remembering syntax.
- Handle a typical DS coding round without needing advanced competitive-programming techniques.

---

# 1. Priority: The Core 50%

The highest-value preparation area is:

1. Hashing / Hash Maps / Sets
2. Arrays
3. Two Pointers
4. Sliding Window
5. Binary Search

These topics should receive roughly **50% of the total DSA preparation time**.

The objective is not to solve every problem in these categories. Instead, learn the patterns and solve a carefully selected set of representative LeetCode problems.

---

# 2. Hashing / Hash Maps / Sets

## What to recognize

Think of hashing when the problem involves:

- Fast lookup
- Counting frequencies
- Finding duplicates
- Finding pairs
- Grouping items
- Prefix sums + lookup
- Remembering something seen earlier

Typical Python tools:

```python
seen = set()

freq = {}

from collections import defaultdict
freq = defaultdict(int)
```

## LeetCode problem list

### Essential

1. **1. Two Sum**
2. **217. Contains Duplicate**
3. **242. Valid Anagram**
4. **49. Group Anagrams**
5. **347. Top K Frequent Elements**
6. **128. Longest Consecutive Sequence**
7. **560. Subarray Sum Equals K**
8. **238. Product of Array Except Self**

### Additional

9. **36. Valid Sudoku**
10. **202. Happy Number**
11. **205. Isomorphic Strings**
12. **290. Word Pattern**

### Pattern to master

```text
Input
  ↓
Need fast lookup/count/grouping?
  ↓
HashMap / HashSet
```

The most important problems here are:

- Two Sum
- Group Anagrams
- Top K Frequent Elements
- Longest Consecutive Sequence
- Subarray Sum Equals K

---

# 3. Arrays

Arrays overlap heavily with the other categories, so don't treat this as a completely separate topic.

## What to recognize

Learn to identify:

- Single-pass problems
- Prefix/suffix processing
- In-place modification
- Running minimum/maximum
- Kadane-style problems
- Sorting + scanning
- Array transformations

## LeetCode problem list

### Essential

1. **121. Best Time to Buy and Sell Stock**
2. **53. Maximum Subarray**
3. **238. Product of Array Except Self**
4. **189. Rotate Array**
5. **283. Move Zeroes**
6. **88. Merge Sorted Array**
7. **27. Remove Element**
8. **26. Remove Duplicates from Sorted Array**

### Additional

9. **169. Majority Element**
10. **189. Rotate Array**
11. **152. Maximum Product Subarray**
12. **56. Merge Intervals** — useful bridge between arrays/sorting and intervals, although intervals are outside the core 50% list.

### Pattern to master

Ask:

> "Can I solve this in one pass while maintaining some state?"

For example:

```python
current_max
best_max
min_price
running_sum
```

The important goal is recognizing when an O(n) scan replaces an O(n²) brute-force solution.

---

# 4. Two Pointers

## What to recognize

Think two pointers when:

- The array/string is sorted.
- You are examining both ends.
- You need a pair satisfying a condition.
- You need in-place modification.
- You are comparing characters from opposite ends.

Typical structure:

```text
left →          ← right
```

## LeetCode problem list

### Essential

1. **125. Valid Palindrome**
2. **167. Two Sum II - Input Array Is Sorted**
3. **15. 3Sum**
4. **11. Container With Most Water**
5. **283. Move Zeroes**
6. **26. Remove Duplicates from Sorted Array**

### Additional

7. **344. Reverse String**
8. **977. Squares of a Sorted Array**
9. **392. Is Subsequence**
10. **42. Trapping Rain Water** — optional/stretch problem.

### Pattern to master

For sorted arrays:

```text
left = 0
right = n - 1

while left < right:
    ...
```

Don't memorize individual solutions.

Learn to ask:

> "Can I move one pointer intelligently instead of checking every pair?"

---

# 5. Sliding Window

This is one of the highest-value patterns in the entire preparation.

## What to recognize

Think sliding window when the problem asks about:

- Subarrays
- Substrings
- Contiguous elements
- Longest/shortest contiguous region
- A window satisfying some condition
- Fixed-size windows
- Variable-size windows

Two major patterns:

### Fixed window

```text
[-----]
  → →
```

### Variable window

```text
[----------]
 left      right
```

Expand the right side and move the left side when the condition is violated.

## LeetCode problem list

### Essential

1. **643. Maximum Average Subarray I**
2. **3. Longest Substring Without Repeating Characters**
3. **209. Minimum Size Subarray Sum**
4. **424. Longest Repeating Character Replacement**
5. **567. Permutation in String**
6. **438. Find All Anagrams in a String**

### Additional

7. **1004. Max Consecutive Ones III**
8. **904. Fruit Into Baskets**
9. **76. Minimum Window Substring** — difficult; use as a stretch problem.
10. **1456. Maximum Number of Vowels in a Substring of Given Length**

### Pattern to master

For variable windows:

```python
left = 0

for right in range(len(nums)):
    # add nums[right]

    while window_is_invalid:
        # remove nums[left]
        left += 1

    # update answer
```

The important skill is recognizing:

> "This is a contiguous range, and I can maintain information about the current range."

---

# 6. Binary Search

## What to recognize

Do not restrict binary search to:

> "The array is sorted."

The broader idea is:

> **There is an ordered/monotonic search space, and I can eliminate half of the possibilities at each step.**

## LeetCode problem list

### Essential

1. **704. Binary Search**
2. **35. Search Insert Position**
3. **34. Find First and Last Position of Element in Sorted Array**
4. **33. Search in Rotated Sorted Array**
5. **153. Find Minimum in Rotated Sorted Array**
6. **875. Koko Eating Bananas**

### Additional

7. **69. Sqrt(x)**
8. **74. Search a 2D Matrix**
9. **1011. Capacity To Ship Packages Within D Days**
10. **1539. Kth Missing Positive Number**

### Pattern to master

Basic binary search:

```python
left = 0
right = len(nums) - 1

while left <= right:
    mid = left + (right - left) // 2

    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
```

Then learn the broader pattern:

```text
Can I define:

low = smallest possible answer
high = largest possible answer

and check whether a candidate answer is feasible?

If yes → binary search on the answer.
```

---

# 7. Recommended Order

Do not study these topics randomly.

Use this sequence:

```text
1. Hashing
      ↓
2. Arrays
      ↓
3. Two Pointers
      ↓
4. Sliding Window
      ↓
5. Binary Search
```

Why?

Because the concepts build on each other.

For example:

```text
Arrays
  ↓
Two Pointers
  ↓
Sliding Window
  ↓
HashMap + Sliding Window
```

and:

```text
Sorted Array
  ↓
Binary Search
  ↓
Binary Search on Answer
```

---

# 8. How to Practice Each Problem

Do NOT simply read a solution and move on.

Use this process.

## Attempt 1 — Independent

Give yourself approximately:

**10–15 minutes for Easy**

**20–30 minutes for Medium**

Try to identify:

1. What is the brute-force approach?
2. What is causing the complexity?
3. Which pattern might remove that bottleneck?

---

## Attempt 2 — Hint

If stuck:

- Read the hint.
- Do not immediately read the full solution.
- Try again.

---

## Attempt 3 — Learn

If still stuck:

1. Read the solution.
2. Understand why it works.
3. Close the solution.
4. Reimplement it yourself.
5. Explain the approach aloud.

The last step is important.

---

# 9. Pattern Recognition Training

Create a mental mapping like this:

| Problem signal | First pattern to consider |
|---|---|
| Need fast lookup | HashMap / Set |
| Frequency/counting | HashMap |
| Find duplicate | Set |
| Find pair | HashMap / Two Pointers |
| Sorted array + pair | Two Pointers |
| Opposite ends | Two Pointers |
| Contiguous subarray | Sliding Window |
| Contiguous substring | Sliding Window |
| Longest/shortest contiguous range | Sliding Window |
| Sorted search | Binary Search |
| Search space is monotonic | Binary Search |
| One-pass optimization | Array / running state |
| Prefix sum + target | Prefix Sum + HashMap |

The goal is to look at a problem and think:

> "Which pattern is this?"

before thinking about code.

---

# 10. Suggested Number of Problems

For the core 50%, target approximately:

| Topic | Target |
|---|---:|
| Hashing | 10–12 |
| Arrays | 8–10 |
| Two Pointers | 8–10 |
| Sliding Window | 8–10 |
| Binary Search | 8–10 |
| **Total** | **~42–52 problems** |

There is intentional overlap between categories.

For example:

- Product of Array Except Self → Arrays + Hashing/prefix concepts
- Move Zeroes → Arrays + Two Pointers
- 3Sum → Arrays + Sorting + Two Pointers
- Longest Substring Without Repeating Characters → HashMap + Sliding Window
- Top K Frequent Elements → HashMap + Heap concepts

This overlap is useful because real interview problems often combine patterns.

---

# 11. Repetition Strategy

Don't try to solve 50 problems once.

Use:

### First pass

Solve all selected problems.

### Second pass

After 1–2 weeks, revisit problems you struggled with.

### Third pass

Before interviews, solve a random mixed set without knowing the topic.

The third pass is the most important.

Why?

Because in an interview you won't be told:

> "This is a sliding-window problem."

You need to identify that yourself.

---

# 12. Interview Simulation

Once the core topics are reasonably comfortable:

## Session format

Pick a random problem.

Do not look at the topic.

Set:

**30 minutes**

Then:

1. Clarify assumptions.
2. Explain brute force.
3. Identify optimized approach.
4. Write code.
5. Test edge cases.
6. Explain complexity.

Example communication:

> "The brute-force approach would be O(n²), because we'd compare every pair. We can reduce this to O(n) by storing previously seen values in a hash map."

This communication should become automatic.

---

# 13. What NOT to Spend Time On

For this specific preparation goal, do not spend significant time on:

- Segment Trees
- Fenwick Trees
- Advanced Graph Algorithms
- Advanced Dynamic Programming
- Computational Geometry
- KMP
- Suffix Arrays
- Heavy-Light Decomposition
- Advanced Bit Manipulation
- Rare Competitive Programming Tricks

The objective is interview readiness for a Data Scientist coding round, not competitive-programming mastery.

---

# 14. Final Success Criterion

You are ready to move beyond the core 50% when you can look at an unseen problem and reasonably quickly classify it:

```text
HashMap?
Array?
Two Pointer?
Sliding Window?
Binary Search?
```

and then solve most common Easy problems and a meaningful proportion of Medium problems within the target time.

At that point, move to the next DSA topics rather than endlessly doing more problems from these five categories.

---

# 15. Minimal Daily Routine

If time is limited:

### 45–60 minutes/day

**10 min**
- Review patterns / previously solved problems

**25–35 min**
- Solve one new problem

**10–15 min**
- Review solution or redo a previous problem

### Once per week

Do one:

**45–60 minute mixed mock interview**

without knowing the topics beforehand.

---

# Bottom Line

Your competitive-programming preparation should be **pattern-focused rather than volume-focused**.

The five most important areas for the first stage are:

> **Hashing → Arrays → Two Pointers → Sliding Window → Binary Search**

Master these first.

Do not aim to become a competitive programmer.

Aim to become the Data Scientist who can confidently handle the coding round and move on to the parts of the interview where your data-science and retail experience matter.

---

# 16. How Strongly Should I Focus on the Core 50%?

Based on the preparation goal and the interview patterns discussed, the answer is:

> **Yes — make the Core 50% your main weapon.**

There is an important distinction, however: the Core 50% is the **highest-ROI preparation area**, not a guarantee that every company will ask only these topics.

For Data Scientist interviews, the coding component can be lighter than a Software Engineer / SDE competitive-programming round. Reported interview experiences also show that coding may sit alongside SQL, statistics, machine learning, case studies, and business/retail discussions.

At the same time, some candidates do report questions involving trees, graphs, DP, stacks, or other DSA topics. These appear particularly often in broader software-engineering interviews, so they should not be completely ignored.

## The practical strategy

Use this preparation pyramid:

```text
                 ADVANCED DSA
          DP / Graph / advanced topics
                  Awareness
                       ▲
                       │
             BASIC DSA SAFETY NET
          Trees / Stack / Heap / BFS
                       ▲
                       │
              ★ CORE 50% ★

          Hashing / Hash Maps / Sets
                    Arrays
                Two Pointers
               Sliding Window
                Binary Search
```

The goal is **not equal depth across every DSA topic**.

The goal is to become exceptionally comfortable with the Core 50%, while having enough familiarity with the remaining topics that an unexpected question does not completely derail you.

---

# 17. What the Core 50% Should Mean for Me

Do not stop at being able to say:

> "I know sliding window."

The target is:

```text
Problem appears
      ↓
Recognize pattern within ~1–3 minutes
      ↓
Explain brute force
      ↓
Identify optimized approach
      ↓
Write clean Python
      ↓
Test edge cases
      ↓
Explain complexity
```

This is the level of readiness that should matter for the coding round.

## Target performance

Aim for approximately:

- **Easy:** solve in ~10–15 minutes.
- **Common Medium:** solve in ~25–35 minutes.
- **Unseen problem:** identify likely patterns quickly even if the final solution takes longer.

---

# 18. Evidence From Retail / Product-Company Interview Reports

Reported interview experiences are useful as directional evidence, but they are not guarantees of future interview questions. The exact difficulty and topics can vary by role, interviewer, team, location, and hiring cycle.

The experiences discussed during preparation suggest:

### Walmart / Walmart Global Tech

Reported Data Scientist interview experiences include relatively light Python/coding components alongside SQL, statistics, machine learning, and case-study/business questions.

Reported Walmart coding experiences also include patterns such as:

- Sliding window
- Prefix sum + HashMap
- Two pointers
- Binary search

Other Walmart technical interviews, particularly Software Engineering interviews, have included topics such as:

- Trees / DFS
- Graphs
- Dynamic Programming
- Backtracking

**Important:** Software Engineering interview reports should not automatically be treated as representative of a Data Scientist interview.

### Target

Reported Target technical interviews have included straightforward array/hashmap-style coding questions and problems such as Product of Array Except Self.

Again, the exact interview can vary substantially by role.

### Other retail companies

For companies such as H&M and similar retail/product organizations, do not assume a fixed question set. Use the Core 50% as the high-value foundation and maintain basic familiarity with the remaining DSA areas.

---

# 19. Do Not Misinterpret the Occasional Harder Question

If an interviewer occasionally asks a Tree, Graph, Stack, Backtracking, or DP problem, this does **not** mean the preparation strategy was wrong.

The objective is risk management.

Instead of doing this:

```text
100% effort
→ every DSA topic
→ deep competitive programming
→ months of preparation
```

Use:

```text
~50% effort
→ Core 50% mastered deeply

~10–15% effort
→ Basic safety-net coverage of other DSA topics

Remaining effort
→ SQL / ML / Statistics / Case Studies / Retail / System Design
```

This keeps the coding round from becoming the blocker without allowing DSA preparation to consume the preparation time needed for a Senior Data Scientist interview.

---

# 20. Basic Safety-Net Topics After the Core 50%

Once the Core 50% is strong, do a small number of representative problems from:

### Stack

Target: ~3–4 problems

Know:

- Valid Parentheses
- Min Stack
- Next Greater Element / Daily Temperatures pattern

### Heap

Target: ~3–4 problems

Know:

- Kth Largest Element
- Top K Frequent Elements
- K Closest Points

### Trees

Target: ~4–5 problems

Know:

- Maximum Depth of Binary Tree
- Binary Tree Level Order Traversal
- Validate Binary Search Tree
- Lowest Common Ancestor

### Graphs

Target: ~3–4 problems

Know:

- Number of Islands
- Rotting Oranges
- Course Schedule / basic graph traversal concept

### Dynamic Programming

Target: ~3–4 problems

Know:

- Climbing Stairs
- House Robber
- Coin Change
- Maximum Subarray / basic DP perspective

The purpose is **recognition and basic competence**, not mastery.

---

# 21. My Final DSA Strategy

## Phase 1 — Master the Core 50%

Spend the majority of DSA preparation on:

1. Hashing
2. Arrays
3. Two Pointers
4. Sliding Window
5. Binary Search

Target: **~45–50 carefully selected problems**.

Do not simply complete them once.

---

## Phase 2 — Repeat

Return to problems where:

- You needed a hint.
- You could not identify the pattern.
- You made implementation mistakes.
- Your solution was significantly slower than the optimal approach.

The objective is to convert recognition into automatic behavior.

---

## Phase 3 — Blind Mixed Practice

This is critical.

Do not select a "Sliding Window" problem intentionally.

Instead, pick a random Easy/Medium problem and ask:

> "Which pattern is this?"

This simulates the real interview.

---

## Phase 4 — Build the Safety Net

Spend a smaller amount of time on:

- Stack
- Heap
- Trees
- BFS / DFS
- Graphs
- Basic DP
- Basic backtracking

Do enough representative problems to avoid being completely unfamiliar with these topics.

---

## Phase 5 — Mock Interviews

Practice 30–40 minute sessions where the topic is unknown in advance.

For every problem:

1. Clarify assumptions.
2. Describe brute force.
3. Identify the bottleneck.
4. Propose an optimized approach.
5. Write Python.
6. Test edge cases.
7. State time and space complexity.

---

# 22. The Key Decision

For this preparation, I should **not** ask:

> "Have I completed all of competitive programming?"

Instead ask:

> "If a typical coding problem appears, can I recognize the pattern and solve it confidently enough to get through the round?"

The Core 50% is designed around that question.

---

# 23. Bottom Line

The strategy is:

> **Master the common patterns deeply rather than trying to master competitive programming broadly.**

For my target Data Scientist roles, the first and most important block is:

> **Hashing → Arrays → Two Pointers → Sliding Window → Binary Search**

Then add a **thin safety net** of Stack, Heap, Trees, Graphs, BFS/DFS, and basic DP.

I do not need to become an expert competitive programmer to remove DSA as an interview blocker.

I need to become **fast, reliable, and pattern-oriented on the problems most likely to be relevant to my role.**
