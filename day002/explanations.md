# Day 002: Python Memory Model, Mutability, and Floating Point Precision

### 1. Variables as Labels, Not Boxes
Variables in Python do not store data values directly. Instead, they act as labels or pointers to objects located in memory. Assigning one variable to another (`list_b = list_a`) creates a shared reference to the exact same memory address.

### 2. Mutable vs. Immutable Types
* **Mutable objects** (like lists) can change their contents in place without altering their memory address. Modifying the object through any label updates the single shared instance.
* **Immutable objects** (like strings) cannot be altered after creation. Any operations that seem to modify a string actually generate a brand new string at a completely different memory address, leaving the original unchanged.

### 3. Shallow Copies vs. Deep Copies
* A **shallow copy** (`list.copy()`) creates a new outer list container, but the elements inside still point to the exact same objects as the original list. If those inner elements are mutable (like a list of lists), modifying a nested item affects both the original and the copy.
* A **deep copy** (`copy.deepcopy()`) recursively clones the outer container and all nested objects inside it, making the copy entirely independent of the original.

### 4. Function Arguments and Shared References
When you pass an object into a Python function, the function parameter receives a reference to the original object, not a copy. If the object is mutable, modifications made inside the function directly alter the original object outside the function.

### 5. Mutable Default Arguments (The Trap)
Default parameter values are evaluated exactly once when the function is defined, not when it is executed. If a mutable object like an empty list (`[]`) is used as a default argument, that single list persists across all function calls, accumulating changes over time.

### 6. Binary Floating-Point Precision
Computers store numbers in binary format (base 2). Certain base 10 decimals, like 0.1 and 0.2, cannot be represented precisely in finite binary fractions. This fractional truncation causes small rounding errors during arithmetic operations.

---

# Day 002: Code Behavior Explanations

### Problem 1: Two Names, One List (Mutability Experiment)

#### List Behavior
When you run `list_b = list_a`, both variables point to the same list object in memory. Calling `list_b.append(911)` updates that shared container. Because `list_a` looks at that same memory location, printing `list_a` shows the updated contents. The `id()` values for both variables remain identical before and after the operation.

#### String Behavior
When you run `str_b = str_a`, both variables start out pointing to the same string object. However, strings are immutable. Running `str_b = str_b + "what's up?"` forces Python to create a brand new string object at a new memory location and updates the `str_b` label to point to it. `str_a` remains pointing to the original, untouched memory location, which is why it still prints "john_doe". The `id()` output shows `str_b` moving to a new memory address while `str_a` stays the same.

---

### Problem 2: List of Lists (Deep Copy Experiment)

In the provided script, `copy.deepcopy()` was used to duplicate `list_1`. Because it was a deep copy, Python built a new outer list and completely new nested inner lists. 

When `list_2[1].append("abc")` runs, it only alters the second nested list inside `list_2`. The original `list_1` remains entirely unaffected. The output confirms this independence because `id(list_1) == id(list_2)` and `id(list_1[1]) == id(list_2[1])` both return `False`.

If a shallow copy had been used instead, `id(list_1[1]) == id(list_2[1])` would be `True`, and modifying the inner list of the copy would have altered the original list as well.

---

### Problem 3: Passing Lists into Functions

When you pass the `numbers` list into `add_to_list(my_list)`, the parameter `my_list` becomes an additional label pointing directly to the external `numbers` list object in memory. 

Running `my_list.append("new_item")` alters that shared memory space. Because no copy was made, the changes are preserved and visible when you print `numbers` outside the function, even though the function has no return statement.

---

### Problem 4: The Famous Trap (Mutable Defaults)

#### Why the first version fails
In the function `def add_to_inventory(inventory=[])`, the default list is created once at definition time. Calling `add_to_inventory()` three times with no arguments reuses that exact same list container every single time. As a result, the string "item" accumulates, printing `['item']`, then `['item', 'item']`, and finally `['item', 'item', 'item']`.

#### Why the second version works
To fix this, the default value is set to the immutable placeholder `None`. 
```python
def add_to_inventory(inventory=None):
    if inventory is None:
        inventory = []
    inventory.append("item")
    return inventory
```
The logic inside the function body runs fresh on every individual function call. If no list is passed, `inventory is None` evaluates to `True`, forcing Python to build a genuinely fresh, empty list container `[]` during that specific execution. Consecutive calls no longer share or accumulate data.

---

### Problem 5: Decimal Math and Base 2 Truncation

#### The 0.1 + 0.2 Issue
Running `print(0.1 + 0.2)` outputs `0.30000000000000004` instead of `0.3`. This happens because computers represent numbers using the IEEE 754 binary floating-point standard. Decimal fractions like 0.1 and 0.2 repeat infinitely when converted to binary, similar to how 1/3 repeats infinitely as 0.333333 in base 10. The computer truncates these infinite fractions to fit into a 53-bit memory limit, creating tiny rounding discrepancies that appear when added together.

#### The Banking Solution
A bank cannot tolerate fractional rounding errors because losing a microscopic fraction of a cent over millions of automated interest transactions causes significant financial imbalances. 

To solve this, Python provides the `decimal` module. By passing the numbers as strings into the `Decimal` object, Python performs base 10 fixed-point arithmetic instead of binary floating-point math:
```python
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2')) # Outputs exactly 0.3
```
