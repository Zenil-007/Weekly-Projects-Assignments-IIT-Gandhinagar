# 🧠 Day 9 — Tuples & Sets Analytics Project

### IIT Gandhinagar PG Diploma in AI / ML

This repository contains my **Day-9 take-home assignment** for the **PG Diploma in AI / Machine Learning at IIT Gandhinagar**.

The assignment focuses on advanced usage of **Python tuples and sets** to simulate **real-world product analytics in an e-commerce system**.

---

# 📚 Topics Covered

* Tuple creation
* Single-element tuple gotcha
* Tuple unpacking
* Named Tuples
* Tuples as dictionary keys
* Set creation and operations
* Set methods (`add`, `remove`, `discard`)
* `frozenset`
* Set performance (O(1) lookup)
* Real-world data analysis using sets

---

# 📂 Project Structure

```
week2/day9/tuples_sets/

│
├── product_analytics.ipynb
├── frozenset_bundles.py
├── interview_answers.md
├── ai_jaccard.md
└── README.md
```

---

# 🧠 Part A — Product Analytics Tool

Implemented in **`product_analytics.ipynb`**

This module simulates a **product analytics engine** for an e-commerce platform using **named tuples and sets**.

### Product Named Tuple

```python
from collections import namedtuple

Product = namedtuple("Product", ["id","name","category","price"])
```

### Product Catalog

A catalog of **15 products across 4 categories**:

* Electronics
* Clothing
* Books
* Home

Example product:

```python
Product(1, "Laptop", "Electronics", 75000)
```

---

### Customer Cart Simulation

Five customers have shopping carts represented as **sets of products**.

Example:

```python
customer_1_cart = {product1, product2, product5}
```

Using sets allows **fast operations and deduplication automatically**.

---

### Shopping Behaviour Analysis

The analytics tool computes:

#### Bestsellers

Products appearing in **all carts**

Uses:

```python
set.intersection()
```

---

#### Catalog Reach

Products appearing in **any cart**

Uses:

```python
set.union()
```

---

#### Exclusive Purchases

Products bought **only by customer 1**

Uses:

```python
set difference
```

---

### Product Recommendation Engine

Function:

```python
recommend_products(customer_cart, all_carts)
```

Suggests products other customers purchased but the current customer did not.

Logic:

```
recommendations = union(all_carts) - customer_cart
```

---

### Category Summary

Generates category wise product sets.

Example output:

```
{
 "Electronics": {"Laptop","Phone","Tablet"},
 "Books": {"Clean Code","Python Crash Course"}
}
```

Uses **set comprehension**.

---

# 🚀 Part B — Frozenset Bundle Discount System

Implemented in **`frozenset_bundles.py`**

### What is `frozenset`?

A `frozenset` is an **immutable version of a set**.

Difference between **set vs frozenset**

| Feature               | set | frozenset |
| --------------------- | --- | --------- |
| Mutable               | ✅   | ❌         |
| Can add/remove items  | ✅   | ❌         |
| Can be dictionary key | ❌   | ✅         |

---

### Bundle Discount Dictionary

Example bundle configuration:

```python
bundle_discounts = {
    frozenset({'Electronics','Books'}): 10
}
```

This means if a customer buys items from both categories they receive a **10% discount**.

---

### Bundle Checker

Function:

```python
check_bundle_discount(cart)
```

Steps:

1. Extract categories from cart
2. Check if bundle categories exist
3. Apply corresponding discount

---

### Performance Benchmark

Compared **set vs frozenset creation speed** using:

```python
timeit
```

Executed **100,000 iterations** to observe performance differences.

---

# 💼 Part C — Interview Preparation

Documented in **`interview_answers.md`**

Topics covered:

### Tuple Immutability Trap

Example:

```python
t = ([1,2], [3,4])
t[0][0] = 99
```

Even though tuples are immutable, they can contain **mutable objects** like lists.

---

### Duplicate Detection (O(n))

Function:

```python
find_duplicates(lst)
```

Uses **set tracking** to detect duplicates efficiently.

---

### Debugging Problem

Original buggy function returned elements unique to **only one list**.

Fixed using:

```python
set(a).symmetric_difference(set(b))
```

Correct output:

```
[1,2,4,5]
```

---

# 🤖 Part D — AI Assisted Programming

Documented in **`ai_jaccard.md`**

### AI Prompt

```
Write a Python function that calculates the Jaccard similarity between two sets of strings.
Explain what Jaccard similarity is and where it is used in industry.
```

---

### Jaccard Similarity

Formula:

```
J(A,B) = |A ∩ B| / |A ∪ B|
```

Example:

```python
set_a = {'python','java','sql'}
set_b = {'python','sql','docker','aws'}
```

Similarity result:

```
0.4
```

---

### Industry Applications

Jaccard similarity is widely used in:

* Recommendation systems
* Document similarity in NLP
* Plagiarism detection
* Search engine ranking

---

# 🛠 Technologies Used

* Python 3
* Named Tuples
* Sets & Set Operations
* Frozenset
* Timeit Benchmarking
* Algorithmic Problem Solving

---

# 🎯 Learning Outcomes

Through this assignment I practiced:

* Using **tuples for structured data**
* Leveraging **set theory for analytics**
* Implementing **recommendation logic**
* Understanding **immutable data structures**
* Benchmarking Python operations
* Evaluating AI-generated code

---

# 👨‍💻 Author

**Zenil Roy**
PG Diploma in AI / Machine Learning
IIT Gandhinagar

---

⭐ This repository is part of my journey toward becoming an **AI Engineer and Machine Learning Researcher**.
