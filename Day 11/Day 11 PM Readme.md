# 🛡️ Python Error Handling & Resilient Systems

This project focuses on **building robust Python programs using proper exception handling, logging, retry mechanisms, and resilient file processing**.

The assignment refactors earlier beginner programs (variables, loops, lists, dictionaries, functions) and transforms them into **production-ready scripts capable of handling real-world failures gracefully**.

The project demonstrates key software engineering practices such as:

* Defensive programming
* Exception handling best practices
* Logging and debugging
* Fault-tolerant file processing
* Retry mechanisms with exponential backoff
* AI-assisted development and evaluation

---

# 📂 Project Structure

```
python-error-handling-project/
│
├── programs/
│   ├── safe_age_calculator.py
│   ├── student_lookup.py
│   └── list_average_calculator.py
│
├── resilient_processing/
│   └── file_processor_resilient.py
│
├── ai_retry_decorator/
│   ├── retry_decorator.py
│   └── test_retry.py
│
├── logs/
│   ├── errors.log
│   └── calc_errors.log
│
├── error_handling_checklist.md
│
├── processing_report.json
│
└── README.md
```

---

# 🧠 Part A — Bulletproof Program Refactoring

Earlier Python programs (Days 7–10 topics) were upgraded with **comprehensive exception handling and validation**.

### Improvements Added

✔ Specific exceptions instead of `bare except`
✔ Input validation using `raise`
✔ Use of full exception structure:

```
try
except
else
finally
```

✔ Logging of internal errors
✔ Clear user-friendly messages

---

## Example: Bulletproof Input Handling

Before (No validation):

```
age = int(input("Enter age: "))
print(age + 10)
```

After (Production-style validation):

```
while True:
    try:
        age = int(input("Enter age: "))
        if age < 0 or age > 150:
            raise ValueError("Age must be between 0 and 150")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        print(age + 10)
        break
```

---

# 📊 Part B — Resilient File Processor

File:
`file_processor_resilient.py`

This script processes a directory of CSV files and **continues operating even if some files fail**.

### Features

* Reads multiple CSV files automatically
* Handles corrupted or invalid files
* Logs full error tracebacks
* Skips failed files and continues processing
* Implements retry logic for `PermissionError`
* Generates a processing report

### Retry Logic

If a file fails due to a permission issue:

* Retry up to **3 times**
* Wait **1 second** between retries

---

## Example Processing Report

`processing_report.json`

```
{
  "files_processed": 8,
  "files_failed": 2,
  "error_details": {
    "bad_file.csv": "Traceback ...",
    "locked_file.csv": "PermissionError"
  }
}
```

---

# 💼 Part C — Interview Preparation

The project reinforces key Python concepts commonly asked in technical interviews.

### Topics Covered

* Exception hierarchy
* Safe file operations
* Defensive coding
* Debugging flawed error handling
* Designing reliable software systems

### Example Concept

Execution order of exception blocks:

```
try → except → else → finally
```

or

```
try → else → finally
```

depending on whether an error occurs.

---

# 🤖 Part D — AI-Assisted Development

An AI model was used to generate a **retry decorator with exponential backoff**.

Decorator:

```
@retry(max_attempts=3, delay=1)
```

Functionality:

* Automatically retries failed functions
* Uses exponential backoff between retries
* Preserves function metadata using `functools.wraps`

---

## Example Usage

```
@retry(max_attempts=3, delay=1)
def unstable_function():
    if random.random() < 0.5:
        raise ValueError("Random failure")
```

This simulates real-world failures such as:

* network requests
* API rate limits
* temporary resource locks

---

# 🧰 Technologies Used

Python Standard Library

```
json
csv
logging
traceback
time
random
functools
pathlib
```

No external dependencies required.

---

# ▶️ How to Run

Clone the repository:

```
git clone https://github.com/yourusername/python-error-handling-project.git
cd python-error-handling-project
```

Run programs:

```
python programs/safe_age_calculator.py
python resilient_processing/file_processor_resilient.py
python ai_retry_decorator/test_retry.py
```

---

# 🎯 Learning Outcomes

This project demonstrates practical experience in:

✔ Writing **robust Python code**
✔ Implementing **structured exception handling**
✔ Designing **fault-tolerant systems**
✔ Logging and debugging production issues
✔ Implementing **retry strategies** used in distributed systems
✔ Evaluating **AI-generated code critically**

---

# 👨‍💻 Author

**Zenil Roy**

PG Diploma in AI & Data Science
IIT Gandhinagar

Interests:

* Artificial Intelligence
* Data Science
* Python Systems Engineering
* Reliable Software Design

---

# 📜 License

This project is created for **educational and learning purposes**.
