# Power BI Integration Guide

Connect Modal LLM Evaluator results to Power BI for advanced analytics and dashboards.

## Table of Contents

- [Overview](#overview)
- [Database Export](#database-export)
- [Power BI Connection](#power-bi-connection)
- [Dashboard Templates](#dashboard-templates)
- [Scheduled Refresh](#scheduled-refresh)
- [Best Practices](#best-practices)

---

## Overview

Export evaluation results to a database and connect Power BI for:
- Executive dashboards
- Cost tracking over time
- Model performance trends
- Team collaboration and reporting
- Automated scheduled reports

**Supported Databases:**
- PostgreSQL (Recommended)
- SQL Server / Azure SQL
- MySQL
- SQLite (not recommended for production)

---

## Database Export

### Option 1: PostgreSQL (Recommended)

#### Setup PostgreSQL

**Local Development:**
```bash
# Install PostgreSQL
# macOS
brew install postgresql
brew services start postgresql

# Ubuntu/Debian
sudo apt-get install postgresql
sudo systemctl start postgresql

# Windows
# Download from https://www.postgresql.org/download/windows/
```

**Create Database:**
```sql
-- Connect to PostgreSQL
psql postgres

-- Create database
CREATE DATABASE llm_evaluator;

-- Create user
CREATE USER llm_user WITH ENCRYPTED PASSWORD 'your_secure_password';

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE llm_evaluator TO llm_user;
```

**Connection String:**
```
postgresql://llm_user:your_secure_password@localhost:5432/llm_evaluator
```

#### Export Results

**Method 1: CLI**
```bash
python -m modal run main.py \
  --experiment-name="my-experiment" \
  --export-format="database" \
  --database-url="postgresql://llm_user:password@localhost:5432/llm_evaluator"
```

**Method 2: Python API**
```python
from evaluator import LLMEvaluator

evaluator = LLMEvaluator()
results = evaluator.run(prompts, test_cases, models)

# Export to database
results.export_to_database(
    connection_string="postgresql://llm_user:password@localhost:5432/llm_evaluator"
)
```

**Method 3: Streamlit UI**
1. Run evaluation
2. Go to Results page
3. Click "Export"
4. Select "Database"
5. Enter connection string
6. Click "Export"

---

### Option 2: Azure SQL Database

**Best for:** Enterprise Azure users

#### Setup Azure SQL

1. **Create Azure SQL Database**
   - Azure Portal → SQL databases
   - Create new database
   - Note server name: `myserver.database.windows.net`

2. **Configure Firewall**
   - Add your IP address
   - Or enable "Allow Azure services"

3. **Get Connection String**
   ```
   mssql+pyodbc://username:password@myserver.database.windows.net:1433/dbname?driver=ODBC+Driver+17+for+SQL+Server
   ```

4. **Install Driver**
   ```bash
   # macOS
   brew install msodbcsql17

   # Ubuntu
   curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
   curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
   apt-get update
   ACCEPT_EULA=Y apt-get install msodbcsql17

   # Windows
   # Download from https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
   ```

5. **Export Results**
   ```bash
   python -m modal run main.py \
     --export-format="database" \
     --database-url="mssql+pyodbc://user:pass@server.database.windows.net:1433/db?driver=ODBC+Driver+17+for+SQL+Server"
   ```

---

### Database Schema

The exporter creates these tables:

**`llm_evaluations` (main results table):**
```sql
CREATE TABLE llm_evaluations (
    id SERIAL PRIMARY KEY,
    experiment_name VARCHAR(255),
    experiment_date TIMESTAMP,
    prompt_name VARCHAR(255),
    test_case_id VARCHAR(255),
    model VARCHAR(100),
    provider VARCHAR(50),
    input_text TEXT,
    output_text TEXT,
    expected_output TEXT,
    exact_match BOOLEAN,
    similarity_score DECIMAL(5,4),
    passed BOOLEAN,
    input_tokens INTEGER,
    output_tokens INTEGER,
    total_tokens INTEGER,
    cost DECIMAL(10,6),
    latency_seconds DECIMAL(8,3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**`llm_costs` (cost tracking table):**
```sql
CREATE TABLE llm_costs (
    id SERIAL PRIMARY KEY,
    experiment_name VARCHAR(255),
    provider VARCHAR(50),
    model VARCHAR(100),
    total_evaluations INTEGER,
    total_cost DECIMAL(10,2),
    avg_cost_per_eval DECIMAL(10,6),
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Indexes for Performance:**
```sql
CREATE INDEX idx_experiment_name ON llm_evaluations(experiment_name);
CREATE INDEX idx_model ON llm_evaluations(model);
CREATE INDEX idx_provider ON llm_evaluations(provider);
CREATE INDEX idx_date ON llm_evaluations(experiment_date);
CREATE INDEX idx_passed ON llm_evaluations(passed);
```

---

## Power BI Connection

### Step 1: Install Power BI Desktop

Download from: https://powerbi.microsoft.com/desktop/

**System Requirements:**
- Windows 10 or later
- 1 GB RAM minimum (4 GB recommended)

---

### Step 2: Connect to Database

#### PostgreSQL Connection

1. **Open Power BI Desktop**
2. **Get Data** → **More** → **Database** → **PostgreSQL database**
3. **Enter Connection Details:**
   - Server: `localhost` (or your server address)
   - Database: `llm_evaluator`
4. **Database Credentials:**
   - User name: `llm_user`
   - Password: `your_secure_password`
5. **Select Tables:**
   - ✅ `llm_evaluations`
   - ✅ `llm_costs`
6. **Load Data**

#### Azure SQL Connection

1. **Get Data** → **Azure** → **Azure SQL Database**
2. **Enter Server:**
   - Server: `myserver.database.windows.net`
   - Database: `llm_evaluator`
3. **Authentication:**
   - Database (username/password)
   - Or Azure Active Directory
4. **Select Tables** and **Load**

---

### Step 3: Data Modeling

#### Create Relationships

Power BI should auto-detect, but verify:

```
llm_evaluations.experiment_name → llm_costs.experiment_name
llm_evaluations.provider → llm_costs.provider
```

#### Create Calculated Columns

**Success Rate:**
```DAX
Success Rate =
DIVIDE(
    COUNTROWS(FILTER(llm_evaluations, llm_evaluations[passed] = TRUE)),
    COUNTROWS(llm_evaluations),
    0
) * 100
```

**Average Cost per Evaluation:**
```DAX
Avg Cost = AVERAGE(llm_evaluations[cost])
```

**Total Cost:**
```DAX
Total Cost = SUM(llm_evaluations[cost])
```

**Quality Score (weighted):**
```DAX
Quality Score =
(AVERAGE(llm_evaluations[exact_match]) * 0.5) +
(AVERAGE(llm_evaluations[similarity_score]) * 0.5)
```

**Efficiency Score (quality/cost):**
```DAX
Efficiency =
DIVIDE(
    [Quality Score],
    [Avg Cost],
    0
)
```

#### Create Date Table

```DAX
Calendar =
ADDCOLUMNS(
    CALENDAR(
        DATE(2024, 1, 1),
        DATE(2025, 12, 31)
    ),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMM"),
    "Month Number", MONTH([Date]),
    "Week", WEEKNUM([Date]),
    "Day", DAY([Date]),
    "Weekday", FORMAT([Date], "ddd")
)
```

---

## Dashboard Templates

### Template 1: Executive Summary

**Page Layout:**

```
┌─────────────────────────────────────────────────────┐
│             LLM Evaluation Dashboard                │
│                  Executive Summary                  │
├─────────────────────────────────────────────────────┤
│  Cards (KPIs):                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐│
│  │ $3,421   │ │  94.3%   │ │  12,450  │ │ Claude ││
│  │Total Cost│ │ Success  │ │  Evals   │ │ Winner ││
│  └──────────┘ └──────────┘ └──────────┘ └────────┘│
├─────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌──────────────────────┐   │
│  │ Cost Trend        │  │ Success Rate by Model│   │
│  │ (Line Chart)      │  │ (Bar Chart)          │   │
│  │                   │  │                      │   │
│  └───────────────────┘  └──────────────────────┘   │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌──────────────────────┐   │
│  │ Cost by Provider  │  │ Recent Experiments   │   │
│  │ (Pie Chart)       │  │ (Table)              │   │
│  │                   │  │                      │   │
│  └───────────────────┘  └──────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

**Visuals:**

1. **KPI Cards:**
   - Total Cost (sum of cost)
   - Average Success Rate (avg of passed)
   - Total Evaluations (count of rows)
   - Best Model (max success rate)

2. **Cost Trend Line Chart:**
   - X-axis: Date
   - Y-axis: Total Cost
   - Legend: Provider

3. **Success Rate by Model (Bar Chart):**
   - X-axis: Model
   - Y-axis: Success Rate %
   - Sort: Descending

4. **Cost Distribution (Pie Chart):**
   - Values: Total Cost
   - Legend: Provider

5. **Recent Experiments (Table):**
   - Columns: Experiment, Date, Tests, Success Rate, Cost
   - Sort: Date descending

---

### Template 2: Cost Analysis

**Page Layout:**

```
┌─────────────────────────────────────────────────────┐
│              Cost Analysis Dashboard                │
├─────────────────────────────────────────────────────┤
│  Filters:                                           │
│  [Date Range] [Provider] [Model] [Experiment]      │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐ │
│  │ Cost Over Time (Area Chart)                   │ │
│  │ Stacked by Provider                           │ │
│  └───────────────────────────────────────────────┘ │
├──────────────────────┬──────────────────────────────┤
│  Cost by Provider    │  Cost by Model               │
│  (Donut Chart)       │  (Bar Chart)                 │
│                      │                              │
├──────────────────────┴──────────────────────────────┤
│  ┌───────────────────────────────────────────────┐ │
│  │ Cost Breakdown Table                          │ │
│  │ Provider | Model | Evals | Total | Avg/Eval  │ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

### Template 3: Model Comparison

**Page Layout:**

```
┌─────────────────────────────────────────────────────┐
│            Model Performance Comparison             │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐ │
│  │ Multi-Dimensional Comparison (Radar Chart)    │ │
│  │ Axes: Success, Cost, Speed, Efficiency        │ │
│  └───────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌───────────────────────┐  │
│  │ Quality vs Cost  │  │ Model Ranking Table   │  │
│  │ (Scatter Plot)   │  │                       │  │
│  │                  │  │ Model | Score | Rank  │  │
│  └──────────────────┘  └───────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

### Template 4: Prompt Analysis

**Page Layout:**

```
┌─────────────────────────────────────────────────────┐
│              Prompt Performance Analysis            │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐ │
│  │ Success Rate by Prompt (Bar Chart)            │ │
│  │ Sorted by performance                         │ │
│  └───────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌───────────────────────┐  │
│  │ Cost per Prompt  │  │ Efficiency by Prompt  │  │
│  │ (Column Chart)   │  │ (Quality/Cost)        │  │
│  └──────────────────┘  └───────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────┐ │
│  │ Detailed Prompt Metrics Table                 │ │
│  │ Prompt | Tests | Pass% | Avg Cost | Efficiency│ │
│  └───────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

## Scheduled Refresh

### Power BI Desktop (Manual)

1. **Ribbon** → **Home** → **Refresh**
2. Or set auto-refresh interval:
   - File → Options → Data Load
   - Enable automatic refresh

### Power BI Service (Automated)

**Requirements:**
- Power BI Pro or Premium license
- On-premises data gateway (if database not cloud-accessible)

#### Setup Gateway (if needed)

1. **Download Gateway:**
   - https://powerbi.microsoft.com/gateway/

2. **Install on Server:**
   - Run installer on machine with database access
   - Sign in with Power BI account

3. **Configure Data Source:**
   - Add PostgreSQL/SQL Server connection
   - Enter credentials

#### Schedule Refresh

1. **Publish Dashboard:**
   - Power BI Desktop → File → Publish
   - Select workspace

2. **Configure Refresh:**
   - Power BI Service → Dataset settings
   - Scheduled refresh → Configure

3. **Set Schedule:**
   - Frequency: Daily, Weekly, or Custom
   - Time: Choose refresh times
   - Time zone: Set correctly
   - Send failure notifications: Enable

**Recommended Schedule:**
- Daily at 6 AM (before team starts work)
- After each evaluation run (webhook trigger)

---

## Best Practices

### Data Optimization

1. **Use Incremental Refresh**
   - Only load new data since last refresh
   - Faster refresh times
   - Lower database load

2. **Archive Old Data**
   - Move data older than 90 days to archive table
   - Keep active dashboard performant

3. **Optimize Queries**
   - Use query folding
   - Filter early in query
   - Reduce column count

### Dashboard Design

1. **Keep It Simple**
   - Max 5-7 visuals per page
   - Use white space
   - Consistent colors

2. **Use Filters**
   - Page-level filters
   - Visual-level filters
   - Slicers for user control

3. **Performance**
   - Limit data to last 90 days by default
   - Use aggregations
   - Avoid complex calculated columns

### Security

1. **Row-Level Security (RLS)**
   ```DAX
   [User Email] = USERPRINCIPALNAME()
   ```

2. **Database Security**
   - Use read-only database user
   - Encrypt connection strings
   - Rotate credentials regularly

3. **Power BI Security**
   - Workspace permissions
   - App permissions
   - Sharing controls

---

## Troubleshooting

### Connection Failed

**Error:** "Unable to connect to database"

**Fix:**
- Verify database is running
- Check connection string
- Verify firewall rules
- Test with database client first

---

### Slow Refresh

**Cause:** Large dataset or complex queries

**Fix:**
- Use incremental refresh
- Add database indexes
- Reduce date range
- Optimize DAX queries

---

### Gateway Issues

**Error:** "Data source not found"

**Fix:**
- Restart gateway
- Verify gateway credentials
- Check gateway logs
- Test connection manually

---

### Data Not Updating

**Cause:** Refresh schedule not working

**Fix:**
- Check refresh history
- Verify gateway is online
- Check credentials haven't expired
- Review error notifications

---

## Advanced Features

### Custom Visuals

**Recommended Custom Visuals:**
- Sankey Diagram (flow between prompts/models)
- Word Cloud (from output text)
- Bullet Chart (performance vs target)
- Timeline Slicer (better date filtering)

**Install:**
1. Power BI → Insert → More visuals
2. Import from marketplace
3. Or upload custom .pbiviz file

---

### R/Python Visuals

**Statistical Analysis:**
```python
# Python visual for advanced analytics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# dataset is automatically available as 'dataset'
df = dataset

# Create custom visualization
sns.regplot(x='cost', y='similarity_score', data=df)
plt.title('Cost vs Quality Correlation')
plt.show()
```

---

### Embedded Analytics

**Embed in Web App:**
```html
<iframe
    width="800"
    height="600"
    src="https://app.powerbi.com/view?r=YOUR_REPORT_ID"
    frameborder="0"
    allowFullScreen="true">
</iframe>
```

---

### Power Automate Integration

**Auto-Email Reports:**
1. Power Automate → Create flow
2. Trigger: Scheduled
3. Action: Export Power BI report
4. Action: Send email with attachment

---

## Sample Reports

Download pre-built Power BI templates:
- `templates/powerbi/executive-summary.pbit`
- `templates/powerbi/cost-analysis.pbit`
- `templates/powerbi/model-comparison.pbit`

**Usage:**
1. Download .pbit template
2. Open in Power BI Desktop
3. Enter your database connection
4. Customize as needed

---

## Need Help?

- **Power BI Documentation:** https://docs.microsoft.com/power-bi/
- **Database Issues:** Check database-specific documentation
- **Feature Requests:** Open GitHub issue
- **Support:** hello@gtmvp.com

---

**Happy Analyzing! 📊**
