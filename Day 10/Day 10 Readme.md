# 📦 Day 10 — Python Dictionaries & Data Processing

### IIT Gandhinagar PG Diploma in AI / ML

This repository contains my **Day-10 take-home assignment** for the **PG Diploma in Artificial Intelligence / Machine Learning at IIT Gandhinagar**.

The assignment focuses on **advanced dictionary operations in Python** and simulates real-world **data engineering tasks** such as product catalog management, log analysis, and dictionary-based analytics.

---

# 📚 Topics Covered

* Dictionary creation (`{}`, `dict()`)
* CRUD operations (`.get()`, `.pop()`, `del`)
* Dictionary methods (`keys`, `values`, `items`, `update`, `setdefault`)
* Nested dictionaries
* Dictionary comprehension
* `collections.defaultdict`
* `collections.Counter`
* Dictionary merging (`|`, `**`, `.update()`)
* Handling edge cases with safe dictionary access

---

# 📂 Project Structure

```id="d10struct"
day10/

│
├── day10_assignment.ipynb
├── log_analyzer.py
├── interview_answers.md
├── ai_grade_analysis.md
└── README.md
```

---

# 🧠 Part A — E-Commerce Product Catalog System

Implemented in **`day10_assignment.ipynb`**

This module builds a **nested dictionary-based product catalog** for an e-commerce system.

### Data Structure

```python
catalog = {
    'SKU001': {
        'name': 'Laptop',
        'price': 65000,
        'category': 'electronics',
        'stock': 15,
        'rating': 4.5,
        'tags': ['computer','work']
    }
}
```

The catalog contains **15 products across four categories**:

* Electronics
* Clothing
* Books
* Food

---

### Business Query Functions

The following analytics functions were implemented using **dictionary operations and comprehensions**.

#### 🔎 Search by Tag

Returns products containing a given tag.

Uses:

```python
defaultdict(list)
```

---

#### 📦 Out of Stock Products

Returns all products where stock is zero.

Uses **dictionary comprehension with filtering**.

---

#### 💰 Price Range Filter

Returns products within a given price range.

Example:

```python
price_range(500, 5000)
```

---

#### 📊 Category Summary

Generates statistics per category:

* Product count
* Average price
* Average rating

Example output:

```python
{
 'electronics': {'count': 4, 'avg_price': 33250.0, 'avg_rating': 4.3},
 'books': {'count': 3, 'avg_price': 916.6, 'avg_rating': 4.6}
}
```

---

#### 🏷 Apply Discount

Function:

```python
apply_discount(category, percent)
```

Reduces prices of products in a given category.

---

#### 🔗 Merge Catalogs

Function:

```python
merge_catalogs(catalog1, catalog2)
```

Uses Python dictionary merging:

```python
catalog1 | catalog2
```

---

# 🚀 Part B — Log Analyzer using Counter & defaultdict

Implemented in **`log_analyzer.py`**

This module simulates a **server log analysis system**.

Example log format:

```text
2026-03-10 ERROR database Connection failed
```

Each log line is parsed into:

```python
{
 'timestamp': '2026-03-10',
 'level': 'ERROR',
 'module': 'database',
 'message': 'Connection failed'
}
```

---

### Analytics Performed

#### 📊 Log Level Distribution

Counts occurrences of:

* INFO
* WARNING
* ERROR
* CRITICAL

Using:

```python
Counter()
```

---

#### ⚠ Most Common Errors

Identifies frequently occurring error messages.

Uses:

```python
Counter.most_common()
```

---

#### 🧩 Most Active Modules

Determines which system module generates the most logs.

---

#### 🗂 Error Grouping by Module

Uses:

```python
defaultdict(list)
```

Example:

```python
{
 'database': ['Connection failed', 'Query timeout']
}
```

---

### Generated Summary

Example output:

```python
{
 'total_entries': 7,
 'error_rate': 42.8,
 'top_errors': [('Connection failed', 1)],
 'busiest_module': 'database'
}
```

---

# 💼 Part C — Interview Preparation

Documented in **`interview_answers.md`**

### Dictionary Time Complexity

Average complexity:

| Operation | Complexity |
| --------- | ---------- |
| Lookup    | O(1)       |
| Insert    | O(1)       |
| Delete    | O(1)       |

This is achieved using **hash tables**.

Worst case complexity:

```
O(n)
```

Occurs when **many keys collide into the same hash bucket**.

---

### Group Anagrams Problem

Function:

```python
group_anagrams(words)
```

Groups words that contain the same letters.

Example:

```python
group_anagrams(['eat','tea','tan','ate','nat','bat'])
```

Output:

```python
{
 'aet': ['eat','tea','ate'],
 'ant': ['tan','nat'],
 'abt': ['bat']
}
```

Uses:

```python
defaultdict(list)
```

---

### Debugging Character Frequency

Bug in original code:

* KeyError when character first appears
* Returned only keys instead of `(char,count)` pairs

Fixed using:

```python
freq.get(char,0) + 1
```

and

```python
sorted(freq.items(), key=lambda x: x[1])
```

---

# 🤖 Part D — AI-Augmented Programming

Documented in **`ai_grade_analysis.md`**

### Prompt Used

```
Write a Python function that takes two dictionaries representing student grades from two semesters and produces a merged report showing combined GPA, grade trend, and subjects common to both semesters.
```

---

### Function Output

Example input:

```python
sem1 = {"math":3.5,"physics":3.8,"ai":3.9}
sem2 = {"math":3.7,"physics":3.6,"ml":4.0}
```

Output report includes:

* Combined GPA
* Trend (improving / declining / stable)
* Subjects present in both semesters

---

### Edge Cases Handled

The improved solution:

✔ Uses `.get()` safely
✔ Handles missing subjects
✔ Handles single-semester data
✔ Supports empty dictionaries

---

# 🛠 Technologies Used

* Python 3
* Dictionaries
* Dictionary comprehension
* `collections.defaultdict`
* `collections.Counter`
* Data parsing and analytics

---

# 🎯 Learning Outcomes

Through this assignment I practiced:

* Designing **nested dictionary data structures**
* Writing **data-driven analytics functions**
* Using **defaultdict and Counter effectively**
* Performing **log analysis workflows**
* Understanding **hash table performance**
* Evaluating and improving **AI-generated code**

---

# 👨‍💻 Author

**Zenil Roy**
PG Diploma in Artificial Intelligence / Machine Learning
IIT Gandhinagar

---

⭐ This project is part of my journey toward becoming a **Data Engineer / AI Engineer**.
