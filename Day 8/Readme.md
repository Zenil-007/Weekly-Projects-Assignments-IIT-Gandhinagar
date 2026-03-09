🔐 Secure Password Analyzer & Transaction Analytics (Python)

A Python project that demonstrates secure password evaluation, random password generation, algorithm optimization, and transaction analytics.

This project was built to strengthen core programming skills required for software engineering, data science, and backend roles, including loops, data structures, algorithm optimization, and clean code practices.

🚀 Project Overview

The project contains two major components:

Password Strength Analyzer & Generator

Transaction Analytics Engine (Paytm-style case study)

Both modules demonstrate real-world backend logic and algorithmic thinking.

🔐 Password Strength Analyzer

This module evaluates password strength using multiple security rules commonly used in authentication systems.

Evaluation Criteria
Rule	Points
Password length ≥ 8	+1
Password length ≥ 12	+2
Password length ≥ 16	+3
Contains uppercase letter	+1
Contains lowercase letter	+1
Contains digit	+1
Contains special character	+1
No more than 2 repeated characters	+1
Strength Classification
Score	Strength
0–2	Weak
3–4	Medium
5–6	Strong
7+	Very Strong
Example
Enter password: hello

Strength: 2/7 (Weak)
Missing: uppercase, digit, special character, too short
Try again...
🔑 Password Generator

The project also includes a secure password generator using Python's random module.

Characters used:

string.ascii_letters
string.digits
string.punctuation

Example output:

Generated Password: aT9@qP$7Lm!
Strength Rating: Strong
💰 Transaction Analytics Engine

A simple analytics tool inspired by digital wallet platforms such as Paytm.

The system records transactions and generates basic financial insights.

Features

Continuous transaction input

Credit and debit tracking

High value transaction detection (> ₹10,000)

Transaction bar chart visualization

Summary analytics

Example Output
credit 5000 : *****
debit 2000 : **
credit 12000 : ************

Each * represents ₹1000.

Analytics Generated

Total transactions

Total credits

Total debits

Net balance

Highest transaction

Average transaction amount

🧠 Algorithms & Concepts Demonstrated

This project demonstrates practical usage of:

Python loops (for, while)

Conditional logic

String processing

Random password generation

Set-based optimization

Algorithm complexity analysis

Data aggregation

Example optimization included in the project:

Pair Sum Problem

Brute Force Approach

Time Complexity: O(n²)

Optimized Approach using Hash Set

Time Complexity: O(n)
🐞 Algorithm Debugging Example

The project also demonstrates debugging and optimization of a prime number algorithm.

Optimized Prime Check
Time Complexity: O(√n)

This improves performance compared to the naive O(n) approach.

🤖 AI-Assisted Development

An AI model was used to generate a diamond pattern program using nested loops.

The generated solution was evaluated for:

Spacing accuracy

Code readability

Edge case handling

Algorithmic complexity

The final implementation was improved to handle invalid inputs.

🛠️ Tech Stack

Python 3

Standard Python libraries

random

string

math

No external dependencies required.

📂 Project Structure
project/
│
├── password_analyzer_generator.py
├── transaction_analyzer.py
└── README.md
🎯 Learning Outcomes

Through this project I practiced:

Writing structured Python programs

Implementing secure password validation logic

Algorithm optimization and debugging

Building small analytics tools

Evaluating AI-generated code critically

📈 Future Improvements

Potential enhancements include:

Password entropy calculation

CLI interface using argparse

Data visualization using matplotlib

Persistent transaction storage

Unit testing

👨‍💻 Author

Zenil Roy

Aspiring AI / Data Science Engineer with strong interest in algorithmic thinking, machine learning, and backend systems.

Currently focusing on:

Python

Data Science

AI Systems

Algorithmic Problem Solving
