# 📊 Day 10 (PM) — Python Functions & Analytics Module

### IIT Gandhinagar · PG Diploma in AI / ML

This repository contains my **Day-10 (PM) take-home assignment** for the **PG Diploma in Artificial Intelligence / Machine Learning at IIT Gandhinagar**.

The assignment focuses on **advanced Python function design**, including:

* Function parameters
* `*args` and `**kwargs`
* Type hints (PEP 484)
* Google-style docstrings
* Variable scope (LEGB rule)
* Lambda functions
* Closures
* Python decorators
* Memoization
* AI-assisted programming evaluation

The project simulates **real-world analytics tools used in EdTech and ML systems**.

---

# 📂 Project Structure

```text
day10_pm/

│
├── student_analytics.ipynb
├── decorators_module.py
├── interview_answers.md
├── ai_text_analysis.md
└── README.md
```

---

# 🧠 Part A — Student Performance Analytics Module

Implemented in **`student_analytics.ipynb`**

This module simulates a **student performance analysis system** used by an EdTech platform.

Student data structure:

```python
students = [
    {
        'name': 'Amit',
        'roll': 'R001',
        'marks': {'math': 85, 'python': 92, 'ml': 78},
        'attendance': 0.0
    }
]
```

---

## Key Functions Implemented

### 1️⃣ `create_student()`

Creates a student record using flexible subject marks via `**kwargs`.

```python
create_student("Amit","R001", math=85, python=92, ml=78)
```

---

### 2️⃣ `calculate_gpa()`

Calculates GPA from any number of marks using `*args`.

```python
calculate_gpa(85,92,78)
```

Example output:

```text
8.5
```

---

### 3️⃣ `get_top_performers()`

Returns the **top N students**.

Two ranking modes:

* Overall average
* Subject-specific ranking

Example:

```python
get_top_performers(students, n=1, subject="python")
```

---

### 4️⃣ `generate_report()`

Creates a formatted student report.

Supports optional flags via `**kwargs`:

* `include_grade`
* `include_rank`
* `verbose`

Example output:

```text
Student: Amit (R001)
Average: 85.00
Grade: B
```

---

### 5️⃣ `classify_students()`

Groups students by grade using:

```python
defaultdict(list)
```

Example result:

```python
{
 'A': [...],
 'B': [...],
 'C': [...],
 'D': [...]
}
```

---

# 🚀 Part B — Custom Python Decorators

Implemented decorators from scratch.

Decorators allow **modifying behavior of functions without changing their code**.

---

## ⏱ `@timer`

Measures execution time of a function.

```python
@timer
def slow_function():
    ...
```

Output example:

```text
Execution time: 0.0021 seconds
```

---

## 📜 `@logger`

Logs function name, arguments, and return value.

Example output:

```text
Calling function: add
Arguments: (5, 10)
Return value: 15
```

---

## 🔁 `@retry`

Retries function execution if an exception occurs.

```python
@retry(max_attempts=3)
def unstable_function():
    ...
```

---

# 💼 Part C — Interview Preparation

Documented in **`interview_answers.md`**

Topics covered:

### LEGB Rule

Python variable scope follows:

```text
Local → Enclosing → Global → Built-in
```

Example:

```python
x = 10

def outer():
    x = 20

    def inner():
        print(x)
```

Scope resolution happens **from nearest to farthest**.

---

### Memoization

Implemented a custom memoization decorator to cache expensive function calls.

Example:

```python
@memoize
def fibonacci(n):
```

Without memoization:

```text
O(2^n) complexity
```

With memoization:

```text
O(n)
```

---

### Mutable Default Argument Bug

Original bug:

```python
def add_to_cart(item, cart=[]):
```

Problem:

The same list persists across calls.

Fixed version:

```python
def add_to_cart(item, cart=None):
```

---

# 🤖 Part D — AI Augmented Programming

Prompt used:

```text
Write a Python module with a function called analyze_text(text: str, **options)
that performs word count, sentence count, longest word detection and simple sentiment analysis.
```

---

### AI Generated Logic

Function analyzes text based on optional flags:

* `count_words`
* `count_sentences`
* `find_longest_word`
* `sentiment_simple`

Example:

```python
analyze_text("Python is amazing.", count_words=True)
```

Output:

```python
{
 'word_count': 3,
 'sentence_count': 1,
 'longest_word': 'amazing'
}
```

---

### Improvements Made

The improved version:

✔ Uses `**kwargs` safely
✔ Handles empty text
✔ Avoids monolithic functions
✔ Uses modular analysis logic

---

# 🛠 Technologies Used

* Python 3
* Type Hints (PEP 484)
* Google-style docstrings
* `defaultdict`
* Function decorators
* Closures
* Memoization
* Jupyter Notebook

---

# 🎯 Learning Outcomes

Through this assignment I practiced:

* Designing **clean Python functions**
* Handling flexible parameters (`*args`, `**kwargs`)
* Writing **type-hinted production-style code**
* Understanding **decorators and closures**
* Implementing **memoization optimization**
* Debugging **common Python pitfalls**
* Evaluating and improving **AI-generated code**

---

# 👨‍💻 Author

**Zenil Roy**
PG Diploma in Artificial Intelligence / Machine Learning
IIT Gandhinagar

---

⭐ This project is part of my journey toward becoming an **AI / ML Engineer and Data Engineer**.
