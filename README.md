# Data Engineering Zoomcamp - Homework Solutions

**Author:** Fateme Haghighi  
**Repository:** Data Engineering Zoomcamp 2025

---

## Table of Contents
- [Module 3: Data Warehousing & BigQuery](#module-3-data-warehousing--bigquery)
- [Module 2: Workflow Orchestration](#module-2-workflow-orchestration)

---

# Module 3: Data Warehousing & BigQuery

**Technology:** Google BigQuery, Google Cloud Storage

## Solution Overview

This homework focuses on understanding BigQuery's data warehousing capabilities, including external tables, partitioning, clustering, and columnar storage optimization.

### Data Setup
- **Dataset:** Yellow Taxi Trip Records (January - June 2024)
- **Source:** NYC TLC Trip Record Data (Parquet format)
- **Storage:** Google Cloud Storage bucket: `dezoomcamp_hw3_2025_fateme`
- **BigQuery Project:** `dtc-de-course-485513`
- **BigQuery Dataset:** `zoomcamp`

### Tables Created
1. **External Table:** `yellow_taxi_external` (reads from GCS)
2. **Materialized Table:** `yellow_taxi_materialized` (data in BigQuery)
3. **Partitioned & Clustered Table:** `yellow_taxi_partitioned_clustered`

---

## Module 3 Questions & Answers

### Question 1: Counting Records

**Question:** What is count of records for the 2024 Yellow Taxi Data?

**Answer:** **20,332,093 records**

**SQL Query:**
```sql
SELECT COUNT(*) as total_records
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 1 Answer](pipeline/screenshots/H3_Screenshots/Q1.png)

---

### Question 2: Data Read Estimation

**Question:** What is the estimated amount of data that will be read when counting distinct PULocationIDs on the External Table vs the Materialized Table?

**Answer:** **0 MB for External Table and 155.12 MB for Materialized Table**

**Explanation:**
- External tables show 0 MB because BigQuery cannot estimate data size for external sources (data in GCS)
- Materialized tables show accurate estimates because data is stored in BigQuery with full metadata

**SQL Queries:**
```sql
-- External Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_external`;

-- Materialized Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 2 Answer](screenshots/H3_Screenshots/Q2.png)

---

### Question 3: Understanding Columnar Storage

**Question:** Why are the estimated number of bytes different when querying one column vs two columns?

**Answer:** **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

**Observations:**
- Single column query: **155.12 MB**
- Two column query: **310.24 MB** (exactly double!)

**SQL Queries:**
```sql
-- Query 1: Single column
SELECT PULocationID 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;

-- Query 2: Two columns
SELECT PULocationID, DOLocationID 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 3 Answer](screenshots/H3_Screenshots/Q3.png)

---

### Question 4: Counting Zero Fare Trips

**Question:** How many records have a fare_amount of 0?

**Answer:** **8,333 records**

**SQL Query:**
```sql
SELECT COUNT(*) as zero_fare_trips
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`
WHERE fare_amount = 0;
```

**Result:**

![Question 4 Answer](screenshots/H3_Screenshots/Q4.png)

---

### Question 5: Partitioning and Clustering Strategy

**Question:** What is the best strategy to optimize a table if queries always filter on tpep_dropoff_datetime and order by VendorID?

**Answer:** **Partition by tpep_dropoff_datetime and Cluster on VendorID**

**Rationale:**
- **PARTITION** by the filter column (tpep_dropoff_datetime) to reduce data scanned
- **CLUSTER** by the ordering column (VendorID) for faster sorting

**SQL Implementation:**
```sql
CREATE OR REPLACE TABLE `dtc-de-course-485513.zoomcamp.yellow_taxi_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 5 Answer](screenshots/H3_Screenshots/Q5.png)

---

### Question 6: Partition Benefits

**Question:** What are the estimated bytes when querying distinct VendorIDs for March 1-15, 2024 on the non-partitioned vs partitioned table?

**Answer:** **310.24 MB for non-partitioned table and 26.84 MB for partitioned table**

**Benefit:** Partitioning reduces data scanned by **~11x** (only reads March partitions instead of all 6 months)

**SQL Queries:**
```sql
-- Non-partitioned table
SELECT DISTINCT VendorID
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned table
SELECT DISTINCT VendorID
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_partitioned_clustered`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

**Result:**

![Question 6 Answer](screenshots/H3_Screenshots/Q6.png)

---

### Question 7: External Table Storage

**Question:** Where is the data stored in the External Table?

**Answer:** **GCP Bucket (Google Cloud Storage)**

**Explanation:** External tables don't copy data into BigQuery. They maintain a reference to files in GCS and read from there during query execution.

**Result:**

![Question 7 Answer](screenshots/H3_Screenshots/Q7.png)

---

### Question 8: Clustering Best Practices

**Question:** Is it best practice in BigQuery to always cluster your data?

**Answer:** **False**

**Rationale:** Clustering is beneficial for:
- Large tables (> 1 GB)
- Common filter/sort patterns
- Frequently queried columns

Not recommended for:
- Small tables (overhead not worth it)
- Tables without consistent query patterns
- Frequently updated tables (maintenance costs)

**Result:**

![Question 8 Answer](screenshots/H3_Screenshots/Q8.png)

---

### Question 9: Understanding Table Scans (Bonus)

**Question:** How many bytes does BigQuery estimate for `SELECT COUNT(*)` and why?

**Answer:** **0 B (Bytes)**

**Explanation:** `COUNT(*)` is a metadata-only operation. BigQuery stores table statistics (row count, size, etc.) and can answer this query without scanning any actual data. It simply reads the row count from metadata.

**Comparison:**
```sql
-- Uses metadata only: 0 B
SELECT COUNT(*) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;

-- Requires column scan: 155.12 MB
SELECT COUNT(PULocationID) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 9 Answer](screenshots/H3_Screenshots/Q9.png)

---

## Module 3 Summary

| Question | Answer | Key Concept |
|----------|--------|-------------|
| Q1 | 20,332,093 | Basic aggregation |
| Q2 | 0 MB / 155.12 MB | External vs Materialized tables |
| Q3 | Columnar database explanation | Columnar storage benefits |
| Q4 | 8,333 | Filtering data |
| Q5 | Partition + Cluster | Query optimization strategy |
| Q6 | 310.24 MB / 26.84 MB | Partitioning benefits (11x reduction) |
| Q7 | GCP Bucket | External table storage |
| Q8 | False | When to use clustering |
| Q9 | 0 B | Metadata optimization |

---

## Key Learnings from Module 3

### 1. External vs Materialized Tables
- **External:** Data stays in GCS, no storage cost in BigQuery, slower queries
- **Materialized:** Data copied to BigQuery, faster queries, storage costs apply

### 2. Columnar Storage
- BigQuery only scans columns specified in SELECT clause
- Cost and performance directly related to columns queried

### 3. Partitioning Benefits
- Dramatically reduces data scanned (11x in our example)
- Best for time-series data with date/timestamp filters
- Physical data separation by partition key

### 4. Clustering Benefits
- Improves sort/filter performance within partitions
- Co-locates related data for faster queries
- Works best with high-cardinality columns

### 5. Query Optimization
- `COUNT(*)` uses metadata (0 bytes scanned)
- Column-specific queries require data scanning
- Proper table design = significant cost savings

---

# Module 2: Workflow Orchestration

**Technology:** Kestra

## Solution Overview

I created a single reusable Kestra flow (`homework2_gcp_taxi.yaml`) that processes NYC Taxi data (Yellow and Green) and loads it into Google BigQuery. The flow was used for both individual executions and backfill operations to answer all homework questions.

### Flow Features
- Flexible inputs: `taxi`, `year`, `month`
- File size tracking (Question 1)
- Variable rendering logging (Question 2)
- BigQuery loading with MERGE operations
- Support for backfill processing

---

## Module 2 Questions & Answers

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

![Q1 & Q2 Code](screenshots/H2_Screenshots/Q1_Q2_code_in_flow.png)

**Result:**

![Question 1 Answer](screenshots/H2_Screenshots/Q1.png)

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

![Question 2 Answer](screenshots/H2_Screenshots/Q2.png)

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

![Question 3 Answer](screenshots/H2_Screenshots/Q3.png)

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

![Question 4 Answer](screenshots/H2_Screenshots/Q4.png)

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

![Question 5 Answer](screenshots/H2_Screenshots/Q5.png)

---

### Question 6: Timezone Configuration

**Question:** How to configure timezone to New York in a Schedule trigger?

**Answer:** Add a `timezone` property set to `America/New_York` in the Schedule trigger configuration

**Method:** Used Kestra AI Copilot for verification

**AI Copilot Query:**

![Question 6 - AI Copilot](screenshots/H2_Screenshots/Q6-1.png)

**Code Implementation:**
```yaml
triggers:
  - id: new_york_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 9 * * *"
    timezone: "America/New_York"
```

![Question 6 - Code](screenshots/H2_Screenshots/Q6-2.png)

---

## Module 2 Summary

| Question | Answer | Method |
|----------|--------|--------|
| Q1 | 134.5 MiB | File size task + single execution |
| Q2 | `green_tripdata_2020-04.csv` | Variable rendering with sprintf |
| Q3 | 24,648,499 | Backfill 2020 + BigQuery query |
| Q4 | 1,734,051 | Backfill 2020 + BigQuery query |
| Q5 | 1,925,152 | Backfill March 2021 + BigQuery query |
| Q6 | `timezone: America/New_York` | Kestra AI Copilot |

---

# Module 3: Data Warehousing & BigQuery

**Technology:** Google BigQuery, Google Cloud Storage

## Solution Overview

This homework focuses on understanding BigQuery's data warehousing capabilities, including external tables, partitioning, clustering, and columnar storage optimization.

### Data Setup
- **Dataset:** Yellow Taxi Trip Records (January - June 2024)
- **Source:** NYC TLC Trip Record Data (Parquet format)
- **Storage:** Google Cloud Storage bucket: `dezoomcamp_hw3_2025_fateme`
- **BigQuery Project:** `dtc-de-course-485513`
- **BigQuery Dataset:** `zoomcamp`

### Tables Created
1. **External Table:** `yellow_taxi_external` (reads from GCS)
2. **Materialized Table:** `yellow_taxi_materialized` (data in BigQuery)
3. **Partitioned & Clustered Table:** `yellow_taxi_partitioned_clustered`

---

## Module 3 Questions & Answers

### Question 1: Counting Records

**Question:** What is count of records for the 2024 Yellow Taxi Data?

**Answer:** **20,332,093 records**

**SQL Query:**
```sql
SELECT COUNT(*) as total_records
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 1 Answer](screenshots/H3_Screenshots/Q1.png)

---

### Question 2: Data Read Estimation

**Question:** What is the estimated amount of data that will be read when counting distinct PULocationIDs on the External Table vs the Materialized Table?

**Answer:** **0 MB for External Table and 155.12 MB for Materialized Table**

**Explanation:**
- External tables show 0 MB because BigQuery cannot estimate data size for external sources (data in GCS)
- Materialized tables show accurate estimates because data is stored in BigQuery with full metadata

**SQL Queries:**
```sql
-- External Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_external`;

-- Materialized Table
SELECT COUNT(DISTINCT PULocationID) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 2 Answer](screenshots/H3_Screenshots/Q2.png)

---

### Question 3: Understanding Columnar Storage

**Question:** Why are the estimated number of bytes different when querying one column vs two columns?

**Answer:** **BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

**Observations:**
- Single column query: **155.12 MB**
- Two column query: **310.24 MB** (exactly double!)

**SQL Queries:**
```sql
-- Query 1: Single column
SELECT PULocationID 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;

-- Query 2: Two columns
SELECT PULocationID, DOLocationID 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 3 Answer](screenshots/H3_Screenshots/Q3.png)

---

### Question 4: Counting Zero Fare Trips

**Question:** How many records have a fare_amount of 0?

**Answer:** **8,333 records**

**SQL Query:**
```sql
SELECT COUNT(*) as zero_fare_trips
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`
WHERE fare_amount = 0;
```

**Result:**

![Question 4 Answer](screenshots/H3_Screenshots/Q4.png)

---

### Question 5: Partitioning and Clustering Strategy

**Question:** What is the best strategy to optimize a table if queries always filter on tpep_dropoff_datetime and order by VendorID?

**Answer:** **Partition by tpep_dropoff_datetime and Cluster on VendorID**

**Rationale:**
- **PARTITION** by the filter column (tpep_dropoff_datetime) to reduce data scanned
- **CLUSTER** by the ordering column (VendorID) for faster sorting

**SQL Implementation:**
```sql
CREATE OR REPLACE TABLE `dtc-de-course-485513.zoomcamp.yellow_taxi_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 5 Answer](screenshots/H3_Screenshots/Q5.png)

---

### Question 6: Partition Benefits

**Question:** What are the estimated bytes when querying distinct VendorIDs for March 1-15, 2024 on the non-partitioned vs partitioned table?

**Answer:** **310.24 MB for non-partitioned table and 26.84 MB for partitioned table**

**Benefit:** Partitioning reduces data scanned by **~11x** (only reads March partitions instead of all 6 months)

**SQL Queries:**
```sql
-- Non-partitioned table
SELECT DISTINCT VendorID
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';

-- Partitioned table
SELECT DISTINCT VendorID
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_partitioned_clustered`
WHERE DATE(tpep_dropoff_datetime) BETWEEN '2024-03-01' AND '2024-03-15';
```

**Result:**

![Question 6 Answer](screenshots/H3_Screenshots/Q6.png)

---

### Question 7: External Table Storage

**Question:** Where is the data stored in the External Table?

**Answer:** **GCP Bucket (Google Cloud Storage)**

**Explanation:** External tables don't copy data into BigQuery. They maintain a reference to files in GCS and read from there during query execution.

**Result:**

![Question 7 Answer](screenshots/H3_Screenshots/Q7.png)

---

### Question 8: Clustering Best Practices

**Question:** Is it best practice in BigQuery to always cluster your data?

**Answer:** **False**

**Rationale:** Clustering is beneficial for:
- Large tables (> 1 GB)
- Common filter/sort patterns
- Frequently queried columns

Not recommended for:
- Small tables (overhead not worth it)
- Tables without consistent query patterns
- Frequently updated tables (maintenance costs)

**Result:**

![Question 8 Answer](screenshots/H3_Screenshots/Q8.png)

---

### Question 9: Understanding Table Scans (Bonus)

**Question:** How many bytes does BigQuery estimate for `SELECT COUNT(*)` and why?

**Answer:** **0 B (Bytes)**

**Explanation:** `COUNT(*)` is a metadata-only operation. BigQuery stores table statistics (row count, size, etc.) and can answer this query without scanning any actual data. It simply reads the row count from metadata.

**Comparison:**
```sql
-- Uses metadata only: 0 B
SELECT COUNT(*) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;

-- Requires column scan: 155.12 MB
SELECT COUNT(PULocationID) 
FROM `dtc-de-course-485513.zoomcamp.yellow_taxi_materialized`;
```

**Result:**

![Question 9 Answer](screenshots/H3_Screenshots/Q9.png)

---

## Module 3 Summary

| Question | Answer | Key Concept |
|----------|--------|-------------|
| Q1 | 20,332,093 | Basic aggregation |
| Q2 | 0 MB / 155.12 MB | External vs Materialized tables |
| Q3 | Columnar database explanation | Columnar storage benefits |
| Q4 | 8,333 | Filtering data |
| Q5 | Partition + Cluster | Query optimization strategy |
| Q6 | 310.24 MB / 26.84 MB | Partitioning benefits (11x reduction) |
| Q7 | GCP Bucket | External table storage |
| Q8 | False | When to use clustering |
| Q9 | 0 B | Metadata optimization |

---

## Key Learnings from Module 3

### 1. External vs Materialized Tables
- **External:** Data stays in GCS, no storage cost in BigQuery, slower queries
- **Materialized:** Data copied to BigQuery, faster queries, storage costs apply

### 2. Columnar Storage
- BigQuery only scans columns specified in SELECT clause
- Cost and performance directly related to columns queried

### 3. Partitioning Benefits
- Dramatically reduces data scanned (11x in our example)
- Best for time-series data with date/timestamp filters
- Physical data separation by partition key

### 4. Clustering Benefits
- Improves sort/filter performance within partitions
- Co-locates related data for faster queries
- Works best with high-cardinality columns

### 5. Query Optimization
- `COUNT(*)` uses metadata (0 bytes scanned)
- Column-specific queries require data scanning
- Proper table design = significant cost savings

---

## Project Structure

```
Data-Engineering-zoomcamp/
├── README.md (this file)
├── screenshots/
│   ├── H2_Screenshots/
│   │   ├── Q1.png
│   │   ├── Q2.png
│   │   ├── Q3.png
│   │   ├── Q4.png
│   │   ├── Q5.png
│   │   ├── Q6-1.png
│   │   ├── Q6-2.png
│   │   └── Q1_Q2_code_in_flow.png
│   └── H3_Screenshots/
│       ├── Q1.png
│       ├── Q2.png
│       ├── Q3.png
│       ├── Q4.png
│       ├── Q5.png
│       ├── Q6.png
│       ├── Q7.png
│       ├── Q8.png
│       └── Q9.png
├── pipeline/
│   └── flows/
│       └── homework2_gcp_taxi.yaml
└── terraform/
    └── credentials.json
```

---

## Technologies Used

### Module 2
- **Kestra** - Workflow orchestration
- **Google BigQuery** - Data warehouse
- **Python** - Data processing

### Module 3
- **Google BigQuery** - Data warehouse and analytics
- **Google Cloud Storage** - Data lake
- **Python** - Data loading scripts
- **SQL** - All queries and analysis

---

## Contact

**Fateme Haghighi**  
Data Engineering Zoomcamp 2025

---

*Last Updated: February 8, 2026*