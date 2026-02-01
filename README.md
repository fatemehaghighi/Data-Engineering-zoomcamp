# Data Engineering Zoomcamp - Module 2 Homework

**Author:** Fateme Haghighi  
**Module:** Workflow Orchestration with Kestra

---

## Solution Overview

I created a single reusable Kestra flow (`homework2_gcp_taxi.yaml`) that processes NYC Taxi data (Yellow and Green) and loads it into Google BigQuery. The flow was used for both individual executions and backfill operations to answer all homework questions.

### Flow Features
- Flexible inputs: `taxi`, `year`, `month`
- File size tracking (Question 1)
- Variable rendering logging (Question 2)
- BigQuery loading with MERGE operations
- Support for backfill processing

---

## Questions & Answers

### Question 1: Uncompressed File Size

**Question:** What is the uncompressed file size for Yellow Taxi December 2020?

**Answer:** `134,481,400 bytes` ≈ **134.5 MiB**

**Method:** Single execution with `taxi=yellow`, `year=2020`, `month=12`

**Code Implementation:**
```yaml
  - id: get_file_size
    type: io.kestra.plugin.core.storage.Size
    uri: "{{render(vars.data)}}"

  - id: set_file_size_label
    type: io.kestra.plugin.core.execution.Labels
    labels:
      fileSize: "{{outputs.get_file_size.size}}"
```

**Code in Flow:**

![Q1 & Q2 Code](screenshots/Q1_Q2_code_in_flow.png)

**Result:**

![Question 1 Answer](screenshots/Q1.png)

---

### Question 2: Rendered Variable Value

**Question:** What is the rendered value of `file` when `taxi=green`, `year=2020`, `month=04`?

**Answer:** `green_tripdata_2020-04.csv`

**Method:** Variable rendering with sprintf formatting

**Code Implementation:**
```yaml
variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{sprintf('%02d', inputs.month)}}.csv"

tasks:
  - id: log_rendered_file_variable
    type: io.kestra.plugin.core.log.Log
    message: "Rendered file variable: {{render(vars.file)}}"
```

**Result:**

![Question 2 Answer](screenshots/Q2.png)

---

### Question 3: Yellow Taxi 2020 Total Rows

**Question:** How many rows for Yellow Taxi in all of 2020?

**Answer:** **24,648,499 rows**

**Method:** 
1. Used Kestra backfill: `2020-01-01` to `2020-12-31` with `taxi=yellow`
2. Queried BigQuery:

```sql
SELECT count(*) 
FROM `dtc-de-course-485513.zoomcamp.yellow_tripdata` 
WHERE filename LIKE 'yellow_tripdata_2020%'
```

**Result:**

![Question 3 Answer](screenshots/Q3.png)

---

### Question 4: Green Taxi 2020 Total Rows

**Question:** How many rows for Green Taxi in all of 2020?

**Answer:** **1,734,051 rows**

**Method:**
1. Used Kestra backfill: `2020-01-01` to `2020-12-31` with `taxi=green`
2. Queried BigQuery:

```sql
SELECT count(*) 
FROM `dtc-de-course-485513.zoomcamp.green_tripdata` 
WHERE filename LIKE 'green_tripdata_2020%'
```

**Result:**

![Question 4 Answer](screenshots/Q4.png)

---

### Question 5: Yellow Taxi March 2021

**Question:** How many rows for Yellow Taxi in March 2021?

**Answer:** **1,925,152 rows**

**Method:**
1. Used Kestra backfill: `2021-03-01` to `2021-03-31` with `taxi=yellow`
2. Queried BigQuery:

```sql
SELECT count(*) 
FROM `dtc-de-course-485513.zoomcamp.yellow_tripdata` 
WHERE filename = 'yellow_tripdata_2021-03.csv'
```

**Result:**

![Question 5 Answer](screenshots/Q5.png)

---

### Question 6: Timezone Configuration

**Question:** How to configure timezone to New York in a Schedule trigger?

**Answer:** Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration

**Method:** Used Kestra AI Copilot for verification

**AI Copilot Query:**

![Question 6 - AI Copilot](screenshots/Q6-1.png)

**Code Implementation:**
```yaml
triggers:
  - id: new_york_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: "America/New_York"
```

![Question 6 - Code](screenshots/Q6-2.png)

---

## Summary

| Question | Answer | Method |
|----------|--------|--------|
| Q1 | 134.5 MiB | File size task + single execution |
| Q2 | `green_tripdata_2020-04.csv` | Variable rendering with sprintf |
| Q3 | 24,648,499 | Backfill 2020 + BigQuery query |
| Q4 | 1,734,051 | Backfill 2020 + BigQuery query |
| Q5 | 1,925,152 | Backfill March 2021 + BigQuery query |
| Q6 | `timezone: America/New_York` | Kestra AI Copilot |

---

## Project Structure

```
pipeline/
├── flows/
│   └── homework2_gcp_taxi.yaml
├── screenshots/
│   ├── Q1.png
│   ├── Q2.png
│   ├── Q3.png
│   ├── Q4.png
│   ├── Q5.png
│   ├── Q6-1.png
│   ├── Q6-2.png
│   └── Q1_Q2_code_in_flow.png
└── README.md
```

---

