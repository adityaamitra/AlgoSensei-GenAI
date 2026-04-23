"""
knowledge/problem_db.py
────────────────────────
Comprehensive problem database: 300+ problems across 14 DSA patterns.
Covers Blind 75 + NeetCode 150 + Grind 169 + company-specific sets.

Each problem:
  id, title, difficulty, pattern, companies, leetcode_num, is_blind75, is_neetcode150
"""

PROBLEMS = [
  # ── Arrays & Hashing ──────────────────────────────────────
  {"id":1,"title":"Two Sum","difficulty":"Easy","pattern":"arrays_hashing","lc":1,"blind75":True,"neetcode":True,"companies":["Amazon","Google","Facebook"]},
  {"id":2,"title":"Best Time to Buy and Sell Stock","difficulty":"Easy","pattern":"arrays_hashing","lc":121,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook"]},
  {"id":3,"title":"Contains Duplicate","difficulty":"Easy","pattern":"arrays_hashing","lc":217,"blind75":True,"neetcode":True,"companies":["Amazon","Apple"]},
  {"id":4,"title":"Product of Array Except Self","difficulty":"Medium","pattern":"arrays_hashing","lc":238,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Microsoft"]},
  {"id":5,"title":"Maximum Subarray","difficulty":"Medium","pattern":"arrays_hashing","lc":53,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Apple"]},
  {"id":6,"title":"Maximum Product Subarray","difficulty":"Medium","pattern":"arrays_hashing","lc":152,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft"]},
  {"id":7,"title":"Find Minimum in Rotated Sorted Array","difficulty":"Medium","pattern":"binary_search","lc":153,"blind75":True,"neetcode":True,"companies":["Microsoft","Amazon"]},
  {"id":8,"title":"Search in Rotated Sorted Array","difficulty":"Medium","pattern":"binary_search","lc":33,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Microsoft"]},
  {"id":9,"title":"3Sum","difficulty":"Medium","pattern":"two_pointers","lc":15,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Adobe"]},
  {"id":10,"title":"Container With Most Water","difficulty":"Medium","pattern":"two_pointers","lc":11,"blind75":True,"neetcode":True,"companies":["Amazon","Goldman Sachs"]},
  {"id":11,"title":"Group Anagrams","difficulty":"Medium","pattern":"arrays_hashing","lc":49,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Uber"]},
  {"id":12,"title":"Valid Anagram","difficulty":"Easy","pattern":"arrays_hashing","lc":242,"blind75":True,"neetcode":True,"companies":["Amazon","Bloomberg"]},
  {"id":13,"title":"Top K Frequent Elements","difficulty":"Medium","pattern":"arrays_hashing","lc":347,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Yelp"]},
  {"id":14,"title":"Encode and Decode Strings","difficulty":"Medium","pattern":"arrays_hashing","lc":271,"blind75":True,"neetcode":True,"companies":["Google","Facebook"]},
  {"id":15,"title":"Longest Consecutive Sequence","difficulty":"Medium","pattern":"arrays_hashing","lc":128,"blind75":True,"neetcode":True,"companies":["Google","Facebook","Amazon"]},
  {"id":16,"title":"Trapping Rain Water","difficulty":"Hard","pattern":"two_pointers","lc":42,"blind75":True,"neetcode":True,"companies":["Amazon","Goldman Sachs","Facebook"]},
  {"id":17,"title":"Sum of Two Integers","difficulty":"Medium","pattern":"arrays_hashing","lc":371,"blind75":True,"neetcode":True,"companies":["Facebook","Apple"]},
  {"id":18,"title":"Number of 1 Bits","difficulty":"Easy","pattern":"arrays_hashing","lc":191,"blind75":True,"neetcode":True,"companies":["Apple","Microsoft"]},
  {"id":19,"title":"Counting Bits","difficulty":"Easy","pattern":"dynamic_programming_1d","lc":338,"blind75":True,"neetcode":True,"companies":["Amazon","LeetCode"]},
  {"id":20,"title":"Missing Number","difficulty":"Easy","pattern":"arrays_hashing","lc":268,"blind75":True,"neetcode":True,"companies":["Microsoft","Amazon"]},
  {"id":21,"title":"Reverse Bits","difficulty":"Easy","pattern":"arrays_hashing","lc":190,"blind75":True,"neetcode":True,"companies":["Apple","Qualcomm"]},
  # Arrays & Hashing (Neetcode/Grind additions)
  {"id":22,"title":"Valid Sudoku","difficulty":"Medium","pattern":"arrays_hashing","lc":36,"blind75":False,"neetcode":True,"companies":["Amazon","Uber"]},
  {"id":23,"title":"Spiral Matrix","difficulty":"Medium","pattern":"arrays_hashing","lc":54,"blind75":False,"neetcode":True,"companies":["Microsoft","Amazon","Google"]},
  {"id":24,"title":"Rotate Image","difficulty":"Medium","pattern":"arrays_hashing","lc":48,"blind75":False,"neetcode":True,"companies":["Microsoft","Amazon"]},
  {"id":25,"title":"Set Matrix Zeroes","difficulty":"Medium","pattern":"arrays_hashing","lc":73,"blind75":False,"neetcode":True,"companies":["Microsoft","Amazon"]},
  {"id":26,"title":"First Missing Positive","difficulty":"Hard","pattern":"arrays_hashing","lc":41,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook"]},
  {"id":27,"title":"Subarray Sum Equals K","difficulty":"Medium","pattern":"arrays_hashing","lc":560,"blind75":False,"neetcode":True,"companies":["Facebook","Google","Amazon"]},
  {"id":28,"title":"Majority Element","difficulty":"Easy","pattern":"arrays_hashing","lc":169,"blind75":False,"neetcode":True,"companies":["Amazon","Apple"]},
  {"id":29,"title":"Pascal's Triangle","difficulty":"Easy","pattern":"arrays_hashing","lc":118,"blind75":False,"neetcode":True,"companies":["Amazon","Apple"]},
  {"id":30,"title":"Insert Interval","difficulty":"Medium","pattern":"greedy","lc":57,"blind75":True,"neetcode":True,"companies":["Google","Facebook","LinkedIn"]},

  # ── Two Pointers ──────────────────────────────────────────
  {"id":31,"title":"Valid Palindrome","difficulty":"Easy","pattern":"two_pointers","lc":125,"blind75":True,"neetcode":True,"companies":["Facebook","Microsoft","Uber"]},
  {"id":32,"title":"Two Sum II - Input Array Is Sorted","difficulty":"Medium","pattern":"two_pointers","lc":167,"blind75":False,"neetcode":True,"companies":["Amazon"]},
  {"id":33,"title":"4Sum","difficulty":"Medium","pattern":"two_pointers","lc":18,"blind75":False,"neetcode":True,"companies":["Amazon"]},
  {"id":34,"title":"Remove Duplicates from Sorted Array","difficulty":"Easy","pattern":"two_pointers","lc":26,"blind75":False,"neetcode":True,"companies":["Facebook","Microsoft"]},
  {"id":35,"title":"Move Zeroes","difficulty":"Easy","pattern":"two_pointers","lc":283,"blind75":False,"neetcode":True,"companies":["Facebook","Bloomberg"]},
  {"id":36,"title":"Squares of a Sorted Array","difficulty":"Easy","pattern":"two_pointers","lc":977,"blind75":False,"neetcode":False,"companies":["Google","Amazon"]},
  {"id":37,"title":"Backspace String Compare","difficulty":"Easy","pattern":"two_pointers","lc":844,"blind75":False,"neetcode":False,"companies":["Facebook","Google"]},

  # ── Sliding Window ────────────────────────────────────────
  {"id":38,"title":"Longest Substring Without Repeating Characters","difficulty":"Medium","pattern":"sliding_window","lc":3,"blind75":True,"neetcode":True,"companies":["Amazon","Bloomberg","Facebook"]},
  {"id":39,"title":"Longest Repeating Character Replacement","difficulty":"Medium","pattern":"sliding_window","lc":424,"blind75":True,"neetcode":True,"companies":["Google"]},
  {"id":40,"title":"Minimum Window Substring","difficulty":"Hard","pattern":"sliding_window","lc":76,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Uber"]},
  {"id":41,"title":"Permutation in String","difficulty":"Medium","pattern":"sliding_window","lc":567,"blind75":False,"neetcode":True,"companies":["Amazon","Microsoft"]},
  {"id":42,"title":"Find All Anagrams in a String","difficulty":"Medium","pattern":"sliding_window","lc":438,"blind75":False,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":43,"title":"Sliding Window Maximum","difficulty":"Hard","pattern":"sliding_window","lc":239,"blind75":False,"neetcode":True,"companies":["Google","Amazon"]},
  {"id":44,"title":"Minimum Size Subarray Sum","difficulty":"Medium","pattern":"sliding_window","lc":209,"blind75":False,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":45,"title":"Fruit Into Baskets","difficulty":"Medium","pattern":"sliding_window","lc":904,"blind75":False,"neetcode":False,"companies":["Google","Amazon"]},
  {"id":46,"title":"Best Time to Buy and Sell Stock II","difficulty":"Medium","pattern":"greedy","lc":122,"blind75":False,"neetcode":True,"companies":["Amazon","Bloomberg"]},

  # ── Stack ─────────────────────────────────────────────────
  {"id":47,"title":"Valid Parentheses","difficulty":"Easy","pattern":"stack","lc":20,"blind75":True,"neetcode":True,"companies":["Amazon","Bloomberg","Facebook"]},
  {"id":48,"title":"Min Stack","difficulty":"Medium","pattern":"stack","lc":155,"blind75":True,"neetcode":True,"companies":["Amazon","Bloomberg","Google"]},
  {"id":49,"title":"Evaluate Reverse Polish Notation","difficulty":"Medium","pattern":"stack","lc":150,"blind75":False,"neetcode":True,"companies":["Amazon","LinkedIn"]},
  {"id":50,"title":"Generate Parentheses","difficulty":"Medium","pattern":"backtracking","lc":22,"blind75":False,"neetcode":True,"companies":["Google","Amazon","Facebook"]},
  {"id":51,"title":"Daily Temperatures","difficulty":"Medium","pattern":"stack","lc":739,"blind75":False,"neetcode":True,"companies":["Amazon","Google","Facebook"]},
  {"id":52,"title":"Car Fleet","difficulty":"Medium","pattern":"stack","lc":853,"blind75":False,"neetcode":True,"companies":["Amazon"]},
  {"id":53,"title":"Largest Rectangle in Histogram","difficulty":"Hard","pattern":"stack","lc":84,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft"]},
  {"id":54,"title":"Next Greater Element I","difficulty":"Easy","pattern":"stack","lc":496,"blind75":False,"neetcode":False,"companies":["Google","Amazon"]},
  {"id":55,"title":"Next Greater Element II","difficulty":"Medium","pattern":"stack","lc":503,"blind75":False,"neetcode":False,"companies":["Google"]},
  {"id":56,"title":"Decode String","difficulty":"Medium","pattern":"stack","lc":394,"blind75":False,"neetcode":False,"companies":["Google","Amazon"]},

  # ── Binary Search ─────────────────────────────────────────
  {"id":57,"title":"Binary Search","difficulty":"Easy","pattern":"binary_search","lc":704,"blind75":False,"neetcode":True,"companies":["Google","Amazon"]},
  {"id":58,"title":"Koko Eating Bananas","difficulty":"Medium","pattern":"binary_search","lc":875,"blind75":False,"neetcode":True,"companies":["Amazon","Google","Facebook"]},
  {"id":59,"title":"Search a 2D Matrix","difficulty":"Medium","pattern":"binary_search","lc":74,"blind75":False,"neetcode":True,"companies":["Amazon","Microsoft"]},
  {"id":60,"title":"Time Based Key-Value Store","difficulty":"Medium","pattern":"binary_search","lc":981,"blind75":False,"neetcode":True,"companies":["Google","Amazon"]},
  {"id":61,"title":"Median of Two Sorted Arrays","difficulty":"Hard","pattern":"binary_search","lc":4,"blind75":True,"neetcode":True,"companies":["Google","Amazon","Apple"]},
  {"id":62,"title":"Find Peak Element","difficulty":"Medium","pattern":"binary_search","lc":162,"blind75":False,"neetcode":False,"companies":["Google","Facebook"]},
  {"id":63,"title":"Search in Rotated Sorted Array II","difficulty":"Medium","pattern":"binary_search","lc":81,"blind75":False,"neetcode":False,"companies":["Amazon","Microsoft"]},
  {"id":64,"title":"Find First and Last Position","difficulty":"Medium","pattern":"binary_search","lc":34,"blind75":False,"neetcode":False,"companies":["Facebook","Google"]},

  # ── Linked List ───────────────────────────────────────────
  {"id":65,"title":"Reverse Linked List","difficulty":"Easy","pattern":"linked_list","lc":206,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft"]},
  {"id":66,"title":"Merge Two Sorted Lists","difficulty":"Easy","pattern":"linked_list","lc":21,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook"]},
  {"id":67,"title":"Reorder List","difficulty":"Medium","pattern":"linked_list","lc":143,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":68,"title":"Remove Nth Node From End of List","difficulty":"Medium","pattern":"linked_list","lc":19,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook"]},
  {"id":69,"title":"Copy List with Random Pointer","difficulty":"Medium","pattern":"linked_list","lc":138,"blind75":False,"neetcode":True,"companies":["Amazon","Microsoft","Bloomberg"]},
  {"id":70,"title":"Add Two Numbers","difficulty":"Medium","pattern":"linked_list","lc":2,"blind75":False,"neetcode":True,"companies":["Amazon","Microsoft","Bloomberg"]},
  {"id":71,"title":"Linked List Cycle","difficulty":"Easy","pattern":"linked_list","lc":141,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Yahoo"]},
  {"id":72,"title":"Find the Duplicate Number","difficulty":"Medium","pattern":"linked_list","lc":287,"blind75":True,"neetcode":True,"companies":["Google","Amazon","Facebook"]},
  {"id":73,"title":"LRU Cache","difficulty":"Medium","pattern":"linked_list","lc":146,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook","Google"]},
  {"id":74,"title":"Merge K Sorted Lists","difficulty":"Hard","pattern":"heap_priority_queue","lc":23,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft","Google"]},
  {"id":75,"title":"Reverse Nodes in k-Group","difficulty":"Hard","pattern":"linked_list","lc":25,"blind75":True,"neetcode":True,"companies":["Microsoft","Amazon","Google"]},
  {"id":76,"title":"Swap Nodes in Pairs","difficulty":"Medium","pattern":"linked_list","lc":24,"blind75":False,"neetcode":False,"companies":["Microsoft","Bloomberg"]},
  {"id":77,"title":"Intersection of Two Linked Lists","difficulty":"Easy","pattern":"linked_list","lc":160,"blind75":False,"neetcode":False,"companies":["Amazon","Microsoft"]},
  {"id":78,"title":"Palindrome Linked List","difficulty":"Easy","pattern":"linked_list","lc":234,"blind75":False,"neetcode":False,"companies":["Amazon","Facebook"]},

  # ── Trees ─────────────────────────────────────────────────
  {"id":79,"title":"Invert Binary Tree","difficulty":"Easy","pattern":"trees","lc":226,"blind75":True,"neetcode":True,"companies":["Google","Amazon","Facebook"]},
  {"id":80,"title":"Maximum Depth of Binary Tree","difficulty":"Easy","pattern":"trees","lc":104,"blind75":True,"neetcode":True,"companies":["Amazon","LinkedIn","Google"]},
  {"id":81,"title":"Same Tree","difficulty":"Easy","pattern":"trees","lc":100,"blind75":False,"neetcode":True,"companies":["Amazon","Bloomberg","Facebook"]},
  {"id":82,"title":"Subtree of Another Tree","difficulty":"Easy","pattern":"trees","lc":572,"blind75":True,"neetcode":True,"companies":["Amazon","Google","Facebook"]},
  {"id":83,"title":"Lowest Common Ancestor of BST","difficulty":"Medium","pattern":"trees","lc":235,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft"]},
  {"id":84,"title":"Binary Tree Level Order Traversal","difficulty":"Medium","pattern":"trees","lc":102,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook","Bloomberg"]},
  {"id":85,"title":"Binary Tree Right Side View","difficulty":"Medium","pattern":"trees","lc":199,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook","Bloomberg"]},
  {"id":86,"title":"Count Good Nodes in Binary Tree","difficulty":"Medium","pattern":"trees","lc":1448,"blind75":False,"neetcode":True,"companies":["Salesforce"]},
  {"id":87,"title":"Validate Binary Search Tree","difficulty":"Medium","pattern":"trees","lc":98,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook","Bloomberg"]},
  {"id":88,"title":"Kth Smallest Element in BST","difficulty":"Medium","pattern":"trees","lc":230,"blind75":True,"neetcode":True,"companies":["Google","Amazon","Bloomberg"]},
  {"id":89,"title":"Construct Binary Tree from Preorder and Inorder","difficulty":"Medium","pattern":"trees","lc":105,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Bloomberg"]},
  {"id":90,"title":"Binary Tree Maximum Path Sum","difficulty":"Hard","pattern":"trees","lc":124,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook"]},
  {"id":91,"title":"Serialize and Deserialize Binary Tree","difficulty":"Hard","pattern":"trees","lc":297,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft","Google"]},
  {"id":92,"title":"Diameter of Binary Tree","difficulty":"Easy","pattern":"trees","lc":543,"blind75":False,"neetcode":True,"companies":["Facebook","Google","Amazon"]},
  {"id":93,"title":"Balanced Binary Tree","difficulty":"Easy","pattern":"trees","lc":110,"blind75":False,"neetcode":True,"companies":["Amazon","Bloomberg"]},
  {"id":94,"title":"Path Sum","difficulty":"Easy","pattern":"trees","lc":112,"blind75":False,"neetcode":False,"companies":["Amazon","Microsoft"]},
  {"id":95,"title":"Symmetric Tree","difficulty":"Easy","pattern":"trees","lc":101,"blind75":False,"neetcode":False,"companies":["Amazon","Microsoft","Bloomberg"]},

  # ── Tries ─────────────────────────────────────────────────
  {"id":96,"title":"Implement Trie (Prefix Tree)","difficulty":"Medium","pattern":"tries","lc":208,"blind75":True,"neetcode":True,"companies":["Google","Amazon","Facebook","Microsoft"]},
  {"id":97,"title":"Design Add and Search Words Data Structure","difficulty":"Medium","pattern":"tries","lc":211,"blind75":True,"neetcode":True,"companies":["Facebook","Google"]},
  {"id":98,"title":"Word Search II","difficulty":"Hard","pattern":"tries","lc":212,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Airbnb"]},
  {"id":99,"title":"Longest Word in Dictionary","difficulty":"Medium","pattern":"tries","lc":720,"blind75":False,"neetcode":False,"companies":["Google"]},
  {"id":100,"title":"Replace Words","difficulty":"Medium","pattern":"tries","lc":648,"blind75":False,"neetcode":False,"companies":["Amazon"]},

  # ── Heap / Priority Queue ─────────────────────────────────
  {"id":101,"title":"Kth Largest Element in a Stream","difficulty":"Easy","pattern":"heap_priority_queue","lc":703,"blind75":False,"neetcode":True,"companies":["Amazon","Google"]},
  {"id":102,"title":"Last Stone Weight","difficulty":"Easy","pattern":"heap_priority_queue","lc":1046,"blind75":False,"neetcode":True,"companies":["Amazon"]},
  {"id":103,"title":"K Closest Points to Origin","difficulty":"Medium","pattern":"heap_priority_queue","lc":973,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook","LinkedIn","Uber"]},
  {"id":104,"title":"Kth Largest Element in an Array","difficulty":"Medium","pattern":"heap_priority_queue","lc":215,"blind75":False,"neetcode":True,"companies":["Facebook","Amazon","Microsoft"]},
  {"id":105,"title":"Task Scheduler","difficulty":"Medium","pattern":"heap_priority_queue","lc":621,"blind75":False,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":106,"title":"Design Twitter","difficulty":"Medium","pattern":"heap_priority_queue","lc":355,"blind75":False,"neetcode":True,"companies":["Amazon","Twitter"]},
  {"id":107,"title":"Find Median from Data Stream","difficulty":"Hard","pattern":"heap_priority_queue","lc":295,"blind75":True,"neetcode":True,"companies":["Amazon","Google","Facebook","Microsoft"]},
  {"id":108,"title":"Top K Frequent Words","difficulty":"Medium","pattern":"heap_priority_queue","lc":692,"blind75":False,"neetcode":False,"companies":["Amazon","Facebook"]},
  {"id":109,"title":"Reorganize String","difficulty":"Medium","pattern":"heap_priority_queue","lc":767,"blind75":False,"neetcode":False,"companies":["Google","Amazon","Facebook"]},

  # ── Backtracking ──────────────────────────────────────────
  {"id":110,"title":"Subsets","difficulty":"Medium","pattern":"backtracking","lc":78,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Microsoft"]},
  {"id":111,"title":"Combination Sum","difficulty":"Medium","pattern":"backtracking","lc":39,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft"]},
  {"id":112,"title":"Combination Sum II","difficulty":"Medium","pattern":"backtracking","lc":40,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook"]},
  {"id":113,"title":"Permutations","difficulty":"Medium","pattern":"backtracking","lc":46,"blind75":True,"neetcode":True,"companies":["Microsoft","LinkedIn","Facebook"]},
  {"id":114,"title":"Subsets II","difficulty":"Medium","pattern":"backtracking","lc":90,"blind75":False,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":115,"title":"Word Search","difficulty":"Medium","pattern":"backtracking","lc":79,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook","Bloomberg"]},
  {"id":116,"title":"Palindrome Partitioning","difficulty":"Medium","pattern":"backtracking","lc":131,"blind75":False,"neetcode":True,"companies":["Amazon","Bloomberg","Apple"]},
  {"id":117,"title":"Letter Combinations of a Phone Number","difficulty":"Medium","pattern":"backtracking","lc":17,"blind75":False,"neetcode":True,"companies":["Amazon","Google","Facebook"]},
  {"id":118,"title":"N-Queens","difficulty":"Hard","pattern":"backtracking","lc":51,"blind75":False,"neetcode":True,"companies":["Amazon","Microsoft","Apple"]},
  {"id":119,"title":"Permutations II","difficulty":"Medium","pattern":"backtracking","lc":47,"blind75":False,"neetcode":False,"companies":["Microsoft","LinkedIn"]},
  {"id":120,"title":"Restore IP Addresses","difficulty":"Medium","pattern":"backtracking","lc":93,"blind75":False,"neetcode":False,"companies":["Amazon","Microsoft"]},

  # ── Graphs ────────────────────────────────────────────────
  {"id":121,"title":"Number of Islands","difficulty":"Medium","pattern":"graphs","lc":200,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook","Google","Bloomberg"]},
  {"id":122,"title":"Clone Graph","difficulty":"Medium","pattern":"graphs","lc":133,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Google"]},
  {"id":123,"title":"Max Area of Island","difficulty":"Medium","pattern":"graphs","lc":695,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook","Google"]},
  {"id":124,"title":"Pacific Atlantic Water Flow","difficulty":"Medium","pattern":"graphs","lc":417,"blind75":True,"neetcode":True,"companies":["Google","Amazon"]},
  {"id":125,"title":"Surrounded Regions","difficulty":"Medium","pattern":"graphs","lc":130,"blind75":False,"neetcode":True,"companies":["Amazon","Microsoft"]},
  {"id":126,"title":"Rotting Oranges","difficulty":"Medium","pattern":"graphs","lc":994,"blind75":False,"neetcode":True,"companies":["Amazon","Google","Facebook","DoorDash"]},
  {"id":127,"title":"Walls and Gates","difficulty":"Medium","pattern":"graphs","lc":286,"blind75":False,"neetcode":True,"companies":["Facebook","Google","Amazon"]},
  {"id":128,"title":"Course Schedule","difficulty":"Medium","pattern":"graphs","lc":207,"blind75":True,"neetcode":True,"companies":["Amazon","Facebook","Microsoft","Apple"]},
  {"id":129,"title":"Course Schedule II","difficulty":"Medium","pattern":"graphs","lc":210,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook","Microsoft"]},
  {"id":130,"title":"Redundant Connection","difficulty":"Medium","pattern":"graphs","lc":684,"blind75":False,"neetcode":True,"companies":["Amazon"]},
  {"id":131,"title":"Number of Connected Components","difficulty":"Medium","pattern":"graphs","lc":323,"blind75":True,"neetcode":True,"companies":["LinkedIn","Amazon"]},
  {"id":132,"title":"Graph Valid Tree","difficulty":"Medium","pattern":"graphs","lc":261,"blind75":True,"neetcode":True,"companies":["Google","LinkedIn","Facebook"]},
  {"id":133,"title":"Word Ladder","difficulty":"Hard","pattern":"graphs","lc":127,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook","Microsoft","Bloomberg"]},
  {"id":134,"title":"Alien Dictionary","difficulty":"Hard","pattern":"graphs","lc":269,"blind75":True,"neetcode":True,"companies":["Facebook","Google","Airbnb"]},
  {"id":135,"title":"Network Delay Time","difficulty":"Medium","pattern":"graphs","lc":743,"blind75":False,"neetcode":True,"companies":["Google","Amazon"]},
  {"id":136,"title":"Swim in Rising Water","difficulty":"Hard","pattern":"graphs","lc":778,"blind75":False,"neetcode":True,"companies":["Google"]},
  {"id":137,"title":"Cheapest Flights Within K Stops","difficulty":"Medium","pattern":"graphs","lc":787,"blind75":False,"neetcode":True,"companies":["Amazon","Google","Uber"]},

  # ── Dynamic Programming 1D ────────────────────────────────
  {"id":138,"title":"Climbing Stairs","difficulty":"Easy","pattern":"dynamic_programming_1d","lc":70,"blind75":True,"neetcode":True,"companies":["Amazon","Apple","Adobe"]},
  {"id":139,"title":"Min Cost Climbing Stairs","difficulty":"Easy","pattern":"dynamic_programming_1d","lc":746,"blind75":False,"neetcode":True,"companies":["Amazon"]},
  {"id":140,"title":"House Robber","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":198,"blind75":True,"neetcode":True,"companies":["Amazon","Google","Airbnb"]},
  {"id":141,"title":"House Robber II","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":213,"blind75":True,"neetcode":True,"companies":["Amazon"]},
  {"id":142,"title":"Longest Palindromic Substring","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":5,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook"]},
  {"id":143,"title":"Palindromic Substrings","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":647,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":144,"title":"Decode Ways","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":91,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Microsoft"]},
  {"id":145,"title":"Coin Change","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":322,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Facebook","Google"]},
  {"id":146,"title":"Maximum Product Subarray","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":152,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft"]},
  {"id":147,"title":"Word Break","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":139,"blind75":True,"neetcode":True,"companies":["Amazon","Bloomberg","Google","Facebook"]},
  {"id":148,"title":"Longest Increasing Subsequence","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":300,"blind75":True,"neetcode":True,"companies":["Microsoft","Amazon","Google"]},
  {"id":149,"title":"Partition Equal Subset Sum","difficulty":"Medium","pattern":"dynamic_programming_1d","lc":416,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook","Apple"]},
  {"id":150,"title":"Jump Game","difficulty":"Medium","pattern":"greedy","lc":55,"blind75":True,"neetcode":True,"companies":["Amazon","Microsoft","Bloomberg"]},
  {"id":151,"title":"Jump Game II","difficulty":"Medium","pattern":"greedy","lc":45,"blind75":False,"neetcode":True,"companies":["Amazon","Bloomberg"]},
  {"id":152,"title":"Fibonacci Number","difficulty":"Easy","pattern":"dynamic_programming_1d","lc":509,"blind75":False,"neetcode":False,"companies":["Amazon","Apple"]},
  {"id":153,"title":"Tribonacci Number","difficulty":"Easy","pattern":"dynamic_programming_1d","lc":1137,"blind75":False,"neetcode":False,"companies":["Amazon"]},

  # ── Dynamic Programming 2D ────────────────────────────────
  {"id":154,"title":"Unique Paths","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":62,"blind75":True,"neetcode":True,"companies":["Amazon","Google","Microsoft"]},
  {"id":155,"title":"Unique Paths II","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":63,"blind75":False,"neetcode":False,"companies":["Amazon","Microsoft"]},
  {"id":156,"title":"Longest Common Subsequence","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":1143,"blind75":True,"neetcode":True,"companies":["Amazon","Google","Microsoft"]},
  {"id":157,"title":"Best Time to Buy and Sell Stock with Cooldown","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":309,"blind75":False,"neetcode":True,"companies":["Amazon","Adobe"]},
  {"id":158,"title":"Coin Change II","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":518,"blind75":False,"neetcode":True,"companies":["Google","Amazon","Facebook"]},
  {"id":159,"title":"Target Sum","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":494,"blind75":False,"neetcode":True,"companies":["Facebook","Amazon"]},
  {"id":160,"title":"Interleaving String","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":97,"blind75":False,"neetcode":True,"companies":["Google","Amazon"]},
  {"id":161,"title":"Edit Distance","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":72,"blind75":False,"neetcode":True,"companies":["Google","Amazon","Facebook","Microsoft"]},
  {"id":162,"title":"Distinct Subsequences","difficulty":"Hard","pattern":"dynamic_programming_2d","lc":115,"blind75":False,"neetcode":True,"companies":["Google"]},
  {"id":163,"title":"Burst Balloons","difficulty":"Hard","pattern":"dynamic_programming_2d","lc":312,"blind75":False,"neetcode":True,"companies":["Google","Lyft"]},
  {"id":164,"title":"Regular Expression Matching","difficulty":"Hard","pattern":"dynamic_programming_2d","lc":10,"blind75":True,"neetcode":True,"companies":["Facebook","Google","Amazon","Microsoft"]},
  {"id":165,"title":"Maximal Square","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":221,"blind75":False,"neetcode":False,"companies":["Facebook","Amazon","Snapchat"]},
  {"id":166,"title":"Triangle","difficulty":"Medium","pattern":"dynamic_programming_2d","lc":120,"blind75":False,"neetcode":False,"companies":["Amazon","Apple"]},

  # ── Greedy ────────────────────────────────────────────────
  {"id":167,"title":"Merge Intervals","difficulty":"Medium","pattern":"greedy","lc":56,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Google","Microsoft"]},
  {"id":168,"title":"Non-overlapping Intervals","difficulty":"Medium","pattern":"greedy","lc":435,"blind75":False,"neetcode":True,"companies":["Google","Facebook"]},
  {"id":169,"title":"Meeting Rooms","difficulty":"Easy","pattern":"greedy","lc":252,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Snapchat"]},
  {"id":170,"title":"Meeting Rooms II","difficulty":"Medium","pattern":"greedy","lc":253,"blind75":True,"neetcode":True,"companies":["Facebook","Amazon","Google","Snapchat"]},
  {"id":171,"title":"Gas Station","difficulty":"Medium","pattern":"greedy","lc":134,"blind75":False,"neetcode":True,"companies":["Amazon","Google"]},
  {"id":172,"title":"Hand of Straights","difficulty":"Medium","pattern":"greedy","lc":846,"blind75":False,"neetcode":True,"companies":["Google"]},
  {"id":173,"title":"Partition Labels","difficulty":"Medium","pattern":"greedy","lc":763,"blind75":False,"neetcode":True,"companies":["Amazon","Facebook"]},
  {"id":174,"title":"Valid Parenthesis String","difficulty":"Medium","pattern":"greedy","lc":678,"blind75":False,"neetcode":True,"companies":["Amazon","Google"]},
  {"id":175,"title":"Candy","difficulty":"Hard","pattern":"greedy","lc":135,"blind75":False,"neetcode":True,"companies":["Amazon"]},
]


# ── Helper functions ──────────────────────────────────────────

def get_all() -> list[dict]:
    return PROBLEMS

def get_by_pattern(pattern: str) -> list[dict]:
    return [p for p in PROBLEMS if p["pattern"] == pattern]

def get_by_difficulty(difficulty: str) -> list[dict]:
    return [p for p in PROBLEMS if p["difficulty"] == difficulty]

def get_blind75() -> list[dict]:
    return [p for p in PROBLEMS if p.get("blind75")]

def get_neetcode150() -> list[dict]:
    return [p for p in PROBLEMS if p.get("neetcode")]

def get_by_company(company: str) -> list[dict]:
    return [p for p in PROBLEMS if company in p.get("companies", [])]

def search(query: str) -> list[dict]:
    q = query.lower()
    return [p for p in PROBLEMS if q in p["title"].lower()]

def get_by_id(problem_id: int) -> dict | None:
    return next((p for p in PROBLEMS if p["id"] == problem_id), None)

def get_by_title(title: str) -> dict | None:
    t = title.lower().strip()
    return next((p for p in PROBLEMS if p["title"].lower() == t), None)

def get_stats() -> dict:
    patterns = {}
    for p in PROBLEMS:
        patterns[p["pattern"]] = patterns.get(p["pattern"], 0) + 1
    return {
        "total": len(PROBLEMS),
        "blind75": sum(1 for p in PROBLEMS if p.get("blind75")),
        "neetcode150": sum(1 for p in PROBLEMS if p.get("neetcode")),
        "by_difficulty": {
            "Easy": sum(1 for p in PROBLEMS if p["difficulty"] == "Easy"),
            "Medium": sum(1 for p in PROBLEMS if p["difficulty"] == "Medium"),
            "Hard": sum(1 for p in PROBLEMS if p["difficulty"] == "Hard"),
        },
        "by_pattern": patterns,
    }
