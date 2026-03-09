# 🧠 Student Management System & Matrix Operations

### IIT Gandhinagar – Weekly Programming Assignment

This repository contains my Python implementation for a **control-flow and data structures assignment** as part of the **PG Diploma in AI / ML from IIT Gandhinagar**.

The assignment demonstrates practical use of:

* Python lists and nested lists
* List comprehensions
* Sorting with lambda functions
* CLI menu-driven applications
* File handling
* Matrix operations using Python lists
* Algorithmic problem solving and debugging
* AI-assisted programming analysis

---

# 📂 Project Structure

```
project/
│
├── student_system.py
├── matrix_ops.py
├── ai_pair_sum.md
└── README.md
```

---

# 🧠 Part A – Student Management System

File: **student_system.py**

A simple **menu-driven CLI application** that manages student records.

### Data Structure

Student records are stored using a **list of lists**.

Example:

```python
[
 ["Aman", "Math", 88],
 ["Priya", "Physics", 91],
 ["Rahul", "Math", 76]
]
```

### Features Implemented

#### 1️⃣ Add Student

* Adds new student record
* Prevents duplicate **name + subject** combinations
* Uses `append()`

#### 2️⃣ Get Toppers

* Returns **Top 3 students per subject**
* Uses:

```python
sorted(records, key=lambda x: x[2], reverse=True)
```

#### 3️⃣ Class Average

* Calculates subject average
* Uses **list comprehension**

Example concept:

```python
[r[2] for r in records if r[1] == subject]
```

#### 4️⃣ Above Average Students

* Calculates overall class average
* Returns students scoring above average

Uses:

* nested logic
* list comprehension

#### 5️⃣ Remove Student

Removes all records of a student.

Uses:

```python
records = [r for r in records if r[0] != name]
```

Avoids modifying lists while iterating.

#### 6️⃣ File Saving

When exiting the program, all records are saved to:

```
students.txt
```

Using Python **file I/O**.

---

# 🚀 Part B – Matrix Operations

File: **matrix_ops.py**

This module implements common matrix operations using Python lists.

### Matrix Addition

Function:

```python
matrix_add(A, B)
```

Example:

```python
A = [[1,2],[3,4]]
B = [[5,6],[7,8]]
```

Output:

```
[[6,8],[10,12]]
```

---

### Matrix Transpose

Function:

```python
matrix_transpose(matrix)
```

Uses **nested list comprehension**.

Example output:

```
[[1,3],
 [2,4]]
```

---

### Matrix Multiplication

Function:

```python
matrix_multiply(A, B)
```

Uses **dot product logic**:

```python
sum(a*b for a,b in zip(row_a,col_b))
```

Handles dimension mismatch safely.

Example output:

```
[[19,22],[43,50]]
```

---

# 💼 Part C – Interview Preparation

This section includes conceptual and coding interview questions.

### Topics Covered

✔ Shallow Copy vs Deep Copy
✔ List Rotation using slicing
✔ Debugging a list modification bug

Example function:

```python
def rotate_list(lst, k):
    k = k % len(lst)
    return lst[-k:] + lst[:-k]
```

---

# 🤖 Part D – AI Augmented Programming

File: **ai_pair_sum.md**

This section demonstrates how AI tools can assist programming.

Steps performed:

1️⃣ Prompted an AI model to generate a pair-sum function
2️⃣ Evaluated the generated code
3️⃣ Identified issues like duplicate pairs
4️⃣ Improved the solution

Improved algorithm uses **sets for O(n) complexity**.

Example improved solution:

```python
def pair_sum(nums, target):

    seen = set()
    pairs = set()

    for num in nums:

        complement = target - num

        if complement in seen:
            pairs.add(tuple(sorted((num, complement))))

        seen.add(num)

    return list(pairs)
```

---

# 🛠 Technologies Used

* Python 3
* Core Python data structures
* CLI programming
* File handling
* Algorithmic problem solving

---

# 🎯 Learning Outcomes

Through this assignment I practiced:

* Python control flow
* Functional problem solving
* Writing modular code
* Using list comprehensions effectively
* Implementing matrix operations manually
* Debugging common Python mistakes
* Evaluating and improving AI generated code

---

# 👨‍💻 Author

Zenil Roy
PG Diploma in AI / ML
IIT Gandhinagar

---

# ⭐ Notes

This project is part of my journey to become an **AI Engineer and Machine Learning Researcher**.

Future improvements may include:

* Converting CLI system to a **web dashboard**
* Adding **database storage**
* Adding **data visualization for student performance**
