# 🧠 Python Data Engineering Mini Pipeline

A Python-based data processing pipeline that merges multiple CSV data sources, removes duplicates, calculates revenue analytics, and exports structured reports.

This project demonstrates **file processing, data cleaning, automation, JSON handling, backup rotation, and filesystem operations** using Python.

---

# 📂 Project Overview

Retail store branches send daily sales CSV files in the following format:

```
date, product, qty, price
```

Example:

```
2025-01-18,Laptop,2,75000
2025-01-18,Mouse,3,500
```

The objective of this project is to:

1. Automatically detect and read multiple CSV files
2. Merge all sales data
3. Remove duplicate records
4. Compute revenue analytics per product
5. Export cleaned data and summarized reports
6. Implement automated file backup with rotation

---

# ⚙️ Features

✔ Automatic CSV file discovery using `pathlib.glob()`
✔ Duplicate row detection and removal
✔ Revenue aggregation per product
✔ Sorted merged dataset export
✔ JSON report generation with metadata
✔ Backup automation with timestamped versions
✔ Backup rotation (keeps only last 5 backups)
✔ Operation logging system

---

# 🏗 Project Structure

```
project-folder/
│
├── data1.csv
├── data2.csv
├── data3.csv
│
├── merged_sales.csv
├── revenue_summary.json
│
├── backup_manager.py
├── backup_log.txt
│
├── csv_to_json_ai_script.py
│
└── README.md
```

---

# 🧠 Part A — Multi-Source Data Merger

This pipeline processes multiple CSV sales files and produces two outputs.

### Steps Performed

1️⃣ Locate CSV files automatically using `pathlib.glob()`
2️⃣ Load all rows using `csv.DictReader`
3️⃣ Remove duplicate rows
4️⃣ Sort records by date
5️⃣ Calculate revenue per product

Revenue Formula:

```
Revenue = qty × price
```

---

# 📄 Output Files

### merged_sales.csv

Contains all **unique sales records** sorted by date.

Example:

```
date,product,qty,price
2025-01-18,Laptop,2,75000
2025-01-18,Mouse,3,500
```

---

### revenue_summary.json

Contains analytics and metadata.

Example:

```json
{
  "metadata": {
    "files_processed": 3,
    "total_rows": 24,
    "total_revenue": 542000.00,
    "generated_at": "2025-01-18T14:30:00"
  },
  "revenue_by_product": {
    "Laptop": 450000.00,
    "Mouse": 9000.00,
    "Keyboard": 16800.00,
    "Monitor": 66000.00
  }
}
```

---

# 🚀 Part B — Backup Manager

The script `backup_manager.py` automates file backups.

### Functionality

* Accepts two arguments

```
python backup_manager.py <source_directory> <backup_directory>
```

* Copies only:

```
.csv
.json
```

* Adds timestamp suffix to backups

Example:

```
sales_20250118_143000.csv
```

* Keeps only **last 5 backups per file**
* Automatically deletes older backups
* Logs all operations to:

```
backup_log.txt
```

---

# 🧪 Example Backup Log

```
Copied data1.csv -> backups/data1_20250118_143000.csv
Copied revenue_summary.json -> backups/revenue_summary_20250118_143000.json
Deleted old backup data1_20250110_120000.csv
```

---

# 💼 Part C — Interview Preparation

This project also demonstrates understanding of key Python concepts.

### Topics Covered

• File handling
• JSON parsing
• Recursive filesystem search
• Sorting algorithms
• Debugging Python scripts
• Memory-safe CSV processing

---

# 🤖 Part D — AI Augmented Development

An AI-generated script was used to convert CSV files into JSON format with automatic delimiter detection.

### Features

• Detects CSV delimiter automatically
• Supports:

```
,
\t
;
|
```

• Converts CSV records into structured JSON output.

---

# 🧰 Technologies Used

Python Standard Library

```
csv
json
pathlib
datetime
shutil
sys
```

No external dependencies required.

---

# ▶️ How to Run

### 1️⃣ Clone Repository

```
git clone https://github.com/yourusername/data-pipeline-project.git
cd data-pipeline-project
```

---

### 2️⃣ Run Data Pipeline

```
python merge_sales.py
```

Outputs:

```
merged_sales.csv
revenue_summary.json
```

---

### 3️⃣ Run Backup Manager

```
python backup_manager.py ./ ./backups
```

---

# 🎯 Learning Outcomes

Through this project I practiced:

✔ File automation using Python
✔ Data cleaning and deduplication
✔ CSV and JSON transformations
✔ Backup automation with rotation
✔ Writing production-style scripts
✔ Integrating AI-generated code responsibly

---

# 👨‍💻 Author

**Zenil Roy**

PG Diploma in AI & Data Science
Python • Data Engineering • AI Systems

---

# 📜 License

This project is created for educational purposes.
