Set-Content -Path "README.md" -Encoding utf8 -Value "# E-Commerce ETL Pipeline

## Overview
End-to-end Data Engineering project สร้าง Modern Data Stack ด้วย Apache Airflow, dbt, PostgreSQL และ Metabase โดยใช้ข้อมูล E-Commerce จริงจาก Kaggle

## Architecture
\`\`\`
Kaggle API
    ↓
Apache Airflow (Orchestration)
    ↓
Extract → Transform → Load
    ↓
PostgreSQL (Data Warehouse)
    ↓
dbt (Transformation + Quality Test)
    ↓
Metabase (Dashboard)
\`\`\`

## Tech Stack
| Tool | Version | Purpose |
|---|---|---|
| Apache Airflow | 2.8.0 | Pipeline Orchestration |
| PostgreSQL | 16 | Data Warehouse |
| dbt | 1.9.0 | Data Transformation |
| Metabase | Latest | Dashboard |
| Docker | - | Containerization |

## Dataset
- Source: [E-Commerce Data - Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data)
- Transactions from UK-based online retailer
- ~500,000 rows

## Pipeline Steps
1. **Extract** — ดึงข้อมูลจาก Kaggle API เก็บเป็นไฟล์ CSV
2. **Transform** — ทำความสะอาดข้อมูลด้วย Python (ลบ null, negative values)
3. **Load** — เก็บข้อมูลลง PostgreSQL
4. **dbt Run** — สร้าง Data Marts ด้วย SQL
5. **dbt Test** — ตรวจสอบคุณภาพข้อมูลอัตโนมัติ

## dbt Models
| Model | Description |
|---|---|
| \`stg_ecom\` | Staging layer - cleaned data |
| \`ecom_monthly_revenue\` | ยอดขายรายเดือน |
| \`ecom_top_product\` | สินค้าขายดี Top 20 |
| \`ecom_top_customers\` | ลูกค้าดีที่สุด Top 20 |
| \`ecom_sales_by_country\` | ยอดขายแยกตามประเทศ |

## Data Quality Tests
- \`not_null\` — ตรวจสอบว่าไม่มีค่า NULL ในคอลัมน์สำคัญ
- \`unique\` — ตรวจสอบความ unique ของ primary keys

## Setup

### Prerequisites
- Docker Desktop
- Kaggle Account + API Key

### Installation
\`\`\`bash
# Clone repo
git clone https://github.com/<your-username>/ecommerce-etl-pipeline.git
cd ecommerce-etl-pipeline

# Add Kaggle credentials
# Create kaggle.json with your API key

# Start services
docker compose up -d

# Download dataset
docker compose exec airflow-webserver kaggle datasets download -d carrie1/ecommerce-data -p /opt/airflow/data --unzip
\`\`\`

### Run Pipeline
1. เปิด Airflow UI ที่ http://localhost:8080
2. Login ด้วย admin/admin
3. เปิด DAG \`etl_ecommerce\`
4. กด Trigger DAG

### View Dashboard
เปิด Metabase ที่ http://localhost:3000"