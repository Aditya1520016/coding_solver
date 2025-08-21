```python
from collections import Counter
from typing import List

class Solution:
    def mostFrequentEven(self, nums: List[int]) -> int:
        even_counts = Counter(num for num in nums if num % 2 == 0)
        if not even_counts:
            return -1
        most_frequent = max(even_counts.values())
        candidates = [num for num, count in even_counts.items() if count == most_frequent]
        return min(candidates)
```