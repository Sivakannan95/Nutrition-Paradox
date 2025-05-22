# ⚖️ Nutrition Paradox: A Global View on Obesity and Malnutrition

## 🌍 Domain
Global Health & Nutrition Analytics

## 📌 Project Summary
This end-to-end data analytics project explores the global double burden of **obesity** and **malnutrition** using publicly available WHO datasets. By performing ETL operations, data cleaning, feature engineering, exploratory analysis, and SQL-based querying, this project offers a deep dive into the nutritional disparities across age groups, genders, countries, and regions. The insights are visualized using either **Power BI** or **Streamlit** dashboards.

---

## 🎯 Skills Gained
- Public API Dataset Extraction
- Data Cleaning and Feature Engineering
- Exploratory Data Analysis (EDA)
- SQL Table Design and Query Writing
- Streamlit or Power BI Dashboard Development
- Health Data Visualization

---

## 📣 Problem Statement
As a Data Analyst at a global health organization, your task is to investigate the complex challenge of **undernutrition** and **overnutrition** across countries. Using WHO data, you'll uncover trends, disparities, and health risks to inform global strategies.

---

## 🔎 Business Use Cases
- **Nutrition Risk Monitoring**: Identify countries with extreme obesity or malnutrition rates.
- **Demographic Disparity Analysis**: Understand gender and age-based differences.
- **Policy Planning**: Support global health policy with data-driven insights.
- **Regional Comparison**: Compare trends across WHO regions.
- **Public Health Reporting**: Enable data-driven storytelling with dashboards.

---

## 📚 Project Approach

### Step 1: Data Collection
Datasets from WHO Global Health Observatory API:
- Obesity (Adults): `NCD_BMI_30C`
- Obesity (Children): `NCD_BMI_PLUS2C`
- Malnutrition (Adults): `NCD_BMI_18C`
- Malnutrition (Children): `NCD_BMI_MINUS2C`

> Filter years: 2012–2022  
> Tools: `requests`, `pandas`, `pycountry`

### Step 2: Data Cleaning & Feature Engineering
- Combine datasets into `df_obesity` and `df_malnutrition`
- Standardize column names and country codes
- Add derived columns:
  - `age_group`, `CI_Width`
  - `obesity_level`, `malnutrition_level` (categorical)

### Step 3: Exploratory Data Analysis (EDA)
- Understand trends by region, gender, and time
- Compare obesity vs malnutrition globally
- Visualizations: Line plots, bar charts, box plots, heatmaps

### Step 4: SQL Integration
- Create MySQL or SQLite database
- Two normalized tables: `obesity_data`, `malnutrition_data`
- Insert records using Python (`.iterrows()` with cursor execution)

### Step 5: Querying & Visualization

#### 🧋 Obesity Table (Sample Queries)
- Top 5 regions with highest obesity in 2022
- India’s obesity trend over years
- Gender-wise obesity averages
- Countries with consistent low obesity

#### 👾 Malnutrition Table (Sample Queries)
- Top 5 countries with highest malnutrition
- Regional trends over time
- CI_Width analysis for data reliability

#### 🔗 Combined Insights
- Obesity vs Malnutrition across 5 countries
- Gender and age-group disparity comparison

### Step 6: Visualization Options
- **Power BI**: Connect to SQL and build dashboard with 20+ visuals
- **Streamlit**: Use `st.selectbox`, `st.dataframe`, `plotly`, and SQL queries to create interactive web app

---

## 🧾 Deliverables
- ✅ Cleaned obesity & malnutrition datasets
- ✅ 25 SQL queries (10 each + 5 combined)
- ✅ EDA visualizations using Python
- ✅ Streamlit App or Power BI Dashboard
- ✅ Summary & Insight Generation report

---

## 🧠 Key Insights
- Which regions need urgent attention?
- Are female obesity rates consistently higher?
- Is child malnutrition still widespread?
- Where does obesity increase while malnutrition drops?

---

## 🛠️ Tech Stack
- Python (pandas, pycountry, matplotlib/seaborn/plotly)
- WHO GHO API
- SQL (MySQL / SQLite / PostgreSQL)
- Power BI / Streamlit
- Jupyter Notebook

---

## 🌐 Tags
`Public Health` `Obesity` `Malnutrition` `SQL` `Power BI` `Python` `ETL` `EDA` `Streamlit` `Global Health` `Feature Engineering`

---

## 📌 How to Run (Optional Instructions)
1. Clone this repo  
2. Run the Jupyter notebook for ETL + EDA  
3. Set up SQL DB and run table creation + insertion scripts  
4. Choose between:
   - `streamlit run app.py` for app demo  
   - Power BI for advanced dashboards  

---

## 📈 Expected Results
- Structured obesity and malnutrition data tables
- 25 insightful SQL queries executed
- Interactive dashboard and rich visual analysis
- Policy-relevant global health insights

---

## 🌟 Conclusion
This project tackles the **"nutrition paradox"** — rising obesity alongside persistent malnutrition. It empowers researchers, policy-makers, and NGOs with data insights to plan more targeted, impactful health interventions globally.
