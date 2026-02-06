# Data Science Salaries Analysis Report

## 1. Introduction
This report analyzes the Data Science Job Salary dataset, focusing on the impact of experience levels on total compensation (in USD).

## 2. Qualitative vs. Quantitative Data
- **Qualitative Data:** `experience_level`, `employment_type`, `job_title`, `salary_currency`, `employee_residence`, `company_location`, `company_size`.
- **Quantitative Data:** `work_year`, `salary`, `salary_in_usd`, `remote_ratio`.

## 3. Preprocessing
- **Missing Values:** No missing values were found in the dataset.
- **Duplicates:** 0 duplicate rows were identified and handled.

## 4. Statistical Analysis
Analysis of `salary_in_usd` grouped by `experience_level`:

| experience_level   |     mean |   median |
|:-------------------|---------:|---------:|
| EX                 | 199392   |   171438 |
| SE                 | 138617   |   135500 |
| MI                 |  87996.1 |    76940 |
| EN                 |  61643.3 |    56500 |

- **EX (Executive):** Commands the highest average and median salaries.
- **SE (Senior):** Follows executive levels as expected.
- **MI (Mid-level):** Occupies the middle ground.
- **EN (Entry-level):** Represents the starting salary tier.

## 5. Visual Insights
The bar chart illustrates a clear positive correlation between experience and salary. The jump from Entry (EN) to Senior (SE) and Executive (EX) is substantial, nearly doubling the average income.

## 6. Reflection
Lack of visualization makes identifying patterns like the skewness in salary (difference between mean and median) harder to digest. Challenges included ensuring the salary was compared in a single currency (USD) to maintain accuracy across global roles.
