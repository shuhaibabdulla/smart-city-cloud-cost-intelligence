# Smart City Cloud Cost Intelligence Platform

## Overview

The **Smart City Cloud Cost Intelligence Platform** is a data analysis project that applies Python, Pandas, and Excel-based workflows to real-world cloud billing management. This project simulates how a Smart City IT department would monitor, analyze, and visualize cloud infrastructure spending using modern DevOps and data analysis tools.

Working with a provided CSV file representing cloud billing data, this project uses Pandas to group and aggregate costs, and generates visual reports in the form of pie charts — all within a professional Jupyter Notebook environment.

---

## Project Objectives

- Analyze cloud billing CSV data using Python and Pandas
- Group cloud costs by **Service Type** and **Month**
- Generate **pie charts** to visualize where the budget is being spent
- Apply data analysis skills in an IT Management and Smart City context
- Demonstrate proficiency in Cloud, DevOps, and data workflows

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and aggregation |
| Excel / CSV | Input data format for cloud billing records |
| Matplotlib / Seaborn | Chart and visualization generation |
| Jupyter Notebook | Interactive development environment |

---

## Project Structure

```
smart-city-cloud-cost-intelligence/
│
├── data/
│   └── cloud_billing.csv          # Sample cloud billing dataset
│
├── notebooks/
│   └── cost_analysis.ipynb        # Main Jupyter Notebook
│
├── outputs/
│   ├── cost_by_service.png        # Pie chart: cost by service type
│   └── cost_by_month.png          # Pie chart: cost by month
│
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## Dataset Description

The provided `cloud_billing.csv` file contains simulated cloud billing records for a Smart City infrastructure environment. The dataset includes the following columns:

| Column | Description |
|---|---|
| `Date` | The billing date of the cloud service usage |
| `Month` | The month extracted from the billing date |
| `Service Type` | Type of cloud service (e.g., Compute, Storage, Networking, AI/ML, Database) |
| `Provider` | Cloud provider (e.g., AWS, Azure, Google Cloud) |
| `Region` | Geographic region of the service deployment |
| `Usage Hours` | Number of hours the service was active |
| `Cost (USD)` | Total cost billed for that entry |

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/shuhaibabdulla/smart-city-cloud-cost-intelligence.git
cd smart-city-cloud-cost-intelligence
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter Notebook

```bash
jupyter notebook
```

Then open `notebooks/cost_analysis.ipynb` and run each cell in order.

---

## Analysis Breakdown

### Step 1 — Load the Data
The billing CSV is loaded into a Pandas DataFrame and inspected for structure, null values, and data types.

### Step 2 — Clean and Prepare
Dates are parsed, months are extracted, and cost columns are converted to numeric format for accurate aggregation.

### Step 3 — Group by Service Type
Costs are summed and grouped by the `Service Type` column to identify which cloud services are consuming the most budget.

### Step 4 — Group by Month
Costs are grouped by `Month` to identify spending trends over time and detect any billing spikes.

### Step 5 — Visualize with Pie Charts
Matplotlib is used to generate clear, labeled pie charts showing the percentage breakdown of costs — both by service and by month.

### Step 6 — Export Results
Charts are saved as PNG files in the `/outputs` folder and can optionally be exported to Excel for reporting.

---

## Sample Visualizations

- **Cost by Service Type** — Shows what percentage of the total cloud bill comes from Compute, Storage, Networking, AI/ML, and Database services
- **Cost by Month** — Shows how cloud spending is distributed across the year, helping identify peak usage periods

---

## Learning Outcomes

By completing this project, students will be able to:

- Load and clean real-world CSV data using Pandas
- Perform groupby aggregations to summarize large datasets
- Create professional pie chart visualizations using Matplotlib
- Understand how cloud billing data is structured in enterprise environments
- Apply IT cost management principles within a Smart City DevOps context
- Document and present data analysis work in Jupyter Notebook format

---

## Requirements

The `requirements.txt` file includes:

```
pandas
matplotlib
openpyxl
jupyter
seaborn
```

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## Academic Context

| Detail | Info |
|---|---|
| **University** | Yenepoya Deemed To Be University |
| **Program** | BCA (AI, Cloud Computing & DevOps) with IBM & TCS |
| **Semester** | VI Semester — Third Year |
| **Academic Year** | 2023–2026 |
| **Subject** | Artificial Intelligence, Cloud Computing and DevOps |
| **Project Type** | Data Analysis and Cloud Cost Management |
| **Tools Used** | Python, Pandas, Excel, Jupyter Notebook |
| **Theme** | Smart City Cloud Infrastructure Management |

---

## Author

**Shuhaib Abdulla**  
BCA (AI, Cloud Computing & DevOps) with IBM & TCS — VI Semester  
Yenepoya Deemed to be University  
GitHub: [@shuhaibabdulla](https://github.com/shuhaibabdulla)

---

## License

This project is submitted for academic purposes at Yenepoya Deemed to be University. All billing data used is simulated and does not represent any real cloud provider's billing records.
