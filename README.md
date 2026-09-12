# Week 2 Task – Data Cleaning and Preprocessing for E-Governance

## 📌 Project Overview

This project demonstrates **data cleaning and preprocessing for e-governance data using Python**. The objective is to transform raw public-sector data into a clean, consistent, and analysis-ready dataset.

The workflow focuses on common data-quality problems such as:

- Missing values
- Duplicate records
- Inconsistent text formatting
- Incorrect data types
- Invalid dates
- Numerical outliers
- Different numerical ranges

The project uses **Pandas and NumPy** and follows a structured preprocessing workflow that can be adapted to real e-governance datasets.

---

## 🎯 Objectives

1. Understand common data-quality issues in public datasets.
2. Detect and handle missing values.
3. Identify and remove duplicate records.
4. Standardize text and date formats.
5. Convert columns to appropriate data types.
6. Detect numerical outliers using the IQR method.
7. Normalize numerical values using Min-Max normalization.
8. Validate the cleaned dataset.
9. Export the final dataset for further analysis or visualization.

---

## 🛠️ Technologies and Libraries

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data loading, cleaning, transformation, and export |
| NumPy | Numerical operations and handling numerical values |
| CSV | Input/output data format |

### Important Pandas Functions Used

- `pd.read_csv()` – loads CSV data
- `df.head()` – previews records
- `df.info()` – checks data types and structure
- `df.isnull().sum()` – detects missing values
- `df.fillna()` – fills missing values
- `df.duplicated()` – detects duplicate rows
- `df.drop_duplicates()` – removes duplicate rows
- `pd.to_datetime()` – converts date values
- `pd.to_numeric()` – converts numerical values
- `df.quantile()` – calculates quartiles for outlier detection
- `df.to_csv()` – exports the cleaned dataset

---

## 📂 Repository Structure

```text
Week-2-E-Governance-Data-Cleaning/
│
├── README.md
├── Week_2_E_Governance_Data_Cleaning_Preprocessing.docx
├── code/
│   └── data_cleaning.py
│
└── cleaned_e_governance_data.csv   # Generated after running the script
```

---

## 🔄 Data Cleaning Workflow

### 1. Load the Dataset

The Python script first attempts to load:

```text
e_governance_data.csv
```

using Pandas:

```python
df = pd.read_csv("e_governance_data.csv")
```

If the input file is not available, the script creates a small sample dataset so that the complete workflow can still be demonstrated.

### 2. Inspect the Dataset

The dataset is inspected using:

```python
df.head()
df.info()
df.describe()
```

This helps identify data types, missing values, and unusual numerical values.

### 3. Handle Missing Values

Missing values are identified with:

```python
df.isnull().sum()
```

For numerical fields such as `applications` and `processing_time`, missing values are replaced with the median:

```python
df["processing_time"] = df["processing_time"].fillna(
    df["processing_time"].median()
)
```

The median is useful when the data may contain extreme values because it is less affected by outliers than the mean.

Categorical missing values can be replaced with:

```python
df["department"] = df["department"].fillna("Unknown")
```

### 4. Remove Duplicate Records

Duplicate records can cause incorrect counts and statistics.

They are detected using:

```python
df.duplicated().sum()
```

and removed using:

```python
df = df.drop_duplicates()
```

### 5. Fix Formatting and Data Types

Text values are standardized by removing unnecessary spaces and applying consistent capitalization:

```python
df["department"] = (
    df["department"]
    .str.strip()
    .str.title()
)
```

Dates are converted to a consistent datetime format:

```python
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

Numerical columns are converted using:

```python
df["applications"] = pd.to_numeric(
    df["applications"], errors="coerce"
)
```

### 6. Detect Outliers

The script uses the **Interquartile Range (IQR)** method.

```python
Q1 = df["applications"].quantile(0.25)
Q3 = df["applications"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
```

Records outside these limits are flagged rather than automatically deleted.

This is important because an unusual value in an e-governance dataset may be a genuine event, such as unusually high demand for a government service.

### 7. Normalize Numerical Data

Min-Max normalization converts numerical values to a range from 0 to 1:

```python
df["applications_normalized"] = (
    (df["applications"] - df["applications"].min())
    / (df["applications"].max() - df["applications"].min())
)
```

This makes numerical variables easier to compare and can be useful for machine-learning algorithms.

### 8. Validate the Cleaned Dataset

After preprocessing, the script checks:

```python
df.isnull().sum()
df.duplicated().sum()
df.dtypes
```

The normalized column is also checked to confirm that its values fall within the expected range.

### 9. Export the Cleaned Dataset

The final dataset is saved using:

```python
df.to_csv(
    "cleaned_e_governance_data.csv",
    index=False
)
```

---

## ▶️ How to Run

### Step 1 – Install Python

Install Python 3.x on your computer.

### Step 2 – Install Required Libraries

Open Command Prompt or Terminal and run:

```bash
pip install pandas numpy
```

### Step 3 – Place the Dataset

If you have the actual e-governance CSV dataset, place it in the same directory as the script and name it:

```text
e_governance_data.csv
```

### Step 4 – Run the Script

From the project directory:

```bash
python code/data_cleaning.py
```

The script will generate:

```text
cleaned_e_governance_data.csv
```

---

## 📊 Expected Output

After execution, the cleaned dataset will contain standardized fields and, where applicable:

- Clean department names
- Converted date values
- Imputed numerical missing values
- Removed duplicate records
- Outlier flags
- Min-Max normalized numerical values

---

## ⚠️ Potential Challenges

Data cleaning requires careful decisions. Missing values should not always be deleted because they may contain useful information. Similarly, an outlier should not automatically be removed because it may represent a real government-service event.

Other challenges include inconsistent department names, invalid dates, incorrect numerical formats, and differences in data collection practices between government departments.

Therefore, every preprocessing decision should be documented and based on the meaning and quality of the data.

---

## ✅ Conclusion

Data cleaning is a critical stage of e-governance data analysis. This project demonstrates how Python, Pandas, and NumPy can be used to identify and resolve common data-quality issues.

The workflow provides a reliable foundation for future **data analysis, Power BI dashboards, statistical analysis, and machine-learning applications**.

---

## 📄 Deliverables

- **Documentation:** `Week_2_E_Governance_Data_Cleaning_Preprocessing.docx`
- **Python script:** `code/data_cleaning.py`
- **Cleaned dataset:** `cleaned_e_governance_data.csv` (generated after execution)

**Week 2 – Data Cleaning and Preprocessing for E-Governance**
