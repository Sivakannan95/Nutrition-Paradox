import streamlit as st
import pandas as pd
import pymysql
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Establish database connection
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='nutrition_paradox'
)
cur = connection.cursor()

# Helper function to run query and return DataFrame
def run_query(query):
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

# Load data for visualizations once
obe_tab = pd.read_sql("SELECT * FROM obesity", connection)
mal_tab = pd.read_sql("SELECT * FROM malnutrition", connection)

# Create 5 tabs
tabs = st.tabs([
    "🧋 Obesity Queries",
    "👾 Malnutrition Queries",
    "🔗 Combined Queries",
    "📊 Visualization",
    "📄 Summary"
])

# ----------------------------------------
# 1. 🧋 Obesity Queries Tab
# ----------------------------------------
with tabs[0]:
    st.header("🧋 Obesity Table Queries")
    obesity_queries = {
        "Top 5 regions with the highest average obesity levels in 2022": '''SELECT * FROM (SELECT region, AVG(mean_estimate) AS avg_ob_level, DENSE_RANK() OVER (ORDER BY AVG(mean_estimate) DESC) AS rnk_ob_level FROM obesity WHERE year = 2022 GROUP BY region) AS ranked WHERE rnk_ob_level <= 5;''',

        "Top 5 countries with highest obesity estimates": '''SELECT * FROM (SELECT country, SUM(mean_estimate) AS obesity_estimates, DENSE_RANK() OVER (ORDER BY SUM(mean_estimate) DESC) AS rnk_obesity FROM obesity GROUP BY country) a WHERE rnk_obesity <= 5''',

        "Obesity trend in India over the years": '''SELECT country, AVG(mean_estimate) AS average_obesity, year FROM obesity WHERE country= 'India' GROUP BY year ORDER BY year''',

        "Average obesity by gender": '''SELECT gender, AVG(mean_estimate) AS average_obesity FROM obesity GROUP BY gender''',

        "Country count by obesity level category and age group": '''SELECT obesity_level, age_group, COUNT(country) AS count_country FROM obesity GROUP BY obesity_level, age_group''',

        "Top 5 least reliable countries (highest CI_Width)": '''SELECT country, AVG(CI_Width) AS avg_ci_width FROM obesity GROUP BY country ORDER BY avg_ci_width DESC LIMIT 5''',

        "Average obesity by age group": '''SELECT age_group, AVG(mean_estimate) AS avg_obesity FROM obesity GROUP BY age_group''',

        "Top 10 consistent low obesity countries": '''SELECT country, ROUND(AVG(mean_estimate), 2) AS avg_obesity, ROUND(AVG(CI_Width), 2) AS avg_ci_width FROM obesity GROUP BY country ORDER BY avg_obesity ASC, avg_ci_width ASC LIMIT 10''',

        "Countries where female obesity exceeds male by large margin": '''SELECT f.country, f.year, ROUND(f.mean_estimate, 2) AS female_obesity, ROUND(m.mean_estimate, 2) AS male_obesity, ROUND(f.mean_estimate - m.mean_estimate, 2) AS obesity_difference FROM obesity f JOIN obesity m ON f.country = m.country AND f.year = m.year WHERE f.gender = 'female' AND m.gender = 'male' AND (f.mean_estimate - m.mean_estimate) > 5 ORDER BY obesity_difference DESC''',

        "Global average obesity percentage per year": '''SELECT year, AVG(mean_estimate) FROM obesity GROUP BY year ORDER BY year'''
    }
    selected_query = st.selectbox("Select an Obesity Query", list(obesity_queries.keys()))
    df = run_query(obesity_queries[selected_query])
    st.dataframe(df)

# ----------------------------------------
# 2. 👾 Malnutrition Queries Tab
# ----------------------------------------
with tabs[1]:
    st.header("👾 Malnutrition Table Queries")
    malnutrition_queries = {
        "Avg. malnutrition by age group": '''SELECT age_group, AVG(mean_estimate) FROM malnutrition GROUP BY age_group''',

        "Top 5 countries with highest malnutrition": '''SELECT country, AVG(mean_estimate) FROM malnutrition GROUP BY country ORDER BY AVG(mean_estimate) DESC LIMIT 5''',

        "Malnutrition trend in African region over the years": '''SELECT region, year, AVG(mean_estimate) FROM malnutrition WHERE region = 'Africa' GROUP BY region, year ORDER BY year''',

        "Gender-based average malnutrition": '''SELECT gender, AVG(mean_estimate) FROM malnutrition GROUP BY gender''',

        "Malnutrition level-wise (avg CI_Width by age group)": '''SELECT malnutrition_level, age_group, AVG(ci_width) FROM malnutrition GROUP BY malnutrition_level, age_group''',

        "Yearly malnutrition change in India, Nigeria, Brazil": '''SELECT year, country, AVG(mean_estimate) FROM malnutrition WHERE country IN ('India', 'Nigeria', 'Brazil') GROUP BY year, country ORDER BY year, country''',

        "Regions with lowest malnutrition averages": '''SELECT region, AVG(mean_estimate) FROM malnutrition GROUP BY region ORDER BY AVG(mean_estimate)''',

        "Countries with increasing malnutrition": '''SELECT country, MIN(mean_estimate) AS earliest_malnutrition, MAX(mean_estimate) AS latest_malnutrition, (MAX(mean_estimate) - MIN(mean_estimate)) AS increase FROM malnutrition GROUP BY country HAVING increase > 0 ORDER BY increase DESC''',

        "Min/Max malnutrition levels year-wise": '''SELECT year, MIN(mean_estimate), MAX(mean_estimate) FROM malnutrition GROUP BY year ORDER BY year''',

        "High CI_Width flags for monitoring (CI_Width > 5)": '''SELECT * FROM malnutrition WHERE ci_width > 5'''
    }
    selected_query = st.selectbox("Select a Malnutrition Query", list(malnutrition_queries.keys()))
    df = run_query(malnutrition_queries[selected_query])
    st.dataframe(df)

# ----------------------------------------
# 3. 🔗 Combined Queries Tab
# ----------------------------------------
with tabs[2]:
    st.header("🔗 Combined Obesity & Malnutrition Queries")
    combined_queries = {
        "Obesity vs malnutrition comparison (any 5 countries)": '''SELECT o.country, AVG(o.mean_estimate) AS obesity_average, AVG(m.mean_estimate) AS malnutrition_average FROM obesity o JOIN malnutrition m ON o.country = m.country GROUP BY o.country LIMIT 5''',

        "Gender-based disparity in obesity & malnutrition": '''WITH avg_ob AS (SELECT gender, AVG(mean_estimate) AS avg_obesity FROM obesity GROUP BY gender), avg_mal AS (SELECT gender, AVG(mean_estimate) AS avg_malnutrition FROM malnutrition GROUP BY gender) SELECT o.gender, o.avg_obesity, m.avg_malnutrition FROM avg_ob o JOIN avg_mal m ON o.gender = m.gender''',

        "Region-wise avg estimates: Africa & America": '''SELECT o.country, AVG(o.mean_estimate) AS obesity_average, AVG(m.mean_estimate) AS malnutrition_average FROM obesity o JOIN malnutrition m ON o.country = m.country WHERE o.country IN ('Africa', 'Americas Region') GROUP BY o.country''',

        "Countries with obesity up & malnutrition down": '''SELECT o.country, MAX(o.mean_estimate) AS high_obesity, MAX(m.mean_estimate) AS low_malnutrition FROM obesity o JOIN malnutrition m ON o.country = m.country GROUP BY o.country''',

        "Age-wise trend analysis": '''SELECT o.age_group, o.year, AVG(o.mean_estimate) AS avg_obesity, AVG(m.mean_estimate) AS avg_malnutrition FROM obesity o JOIN malnutrition m ON o.country = m.country AND o.year = m.year AND o.age_group = m.age_group GROUP BY o.age_group, o.year ORDER BY o.age_group, o.year'''
    }
    selected_query = st.selectbox("Select a Combined Query", list(combined_queries.keys()))
    df = run_query(combined_queries[selected_query])
    st.dataframe(df)

# ----------------------------------------
# 4. 📊 Visualization Tab
# ----------------------------------------
with tabs[3]:
    st.header("📊 Visualizations")

    # 1. Obesity Line Plot
    st.subheader("Global Obesity Trend (Mean Estimate by Year)")
    sam_tab = obe_tab.groupby('year')['mean_estimate'].mean().reset_index()
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=sam_tab, x='year', y='mean_estimate', marker='o', ax=ax1)
    st.pyplot(fig1)

    # 2. Malnutrition Line Plot
    st.subheader("Global Malnutrition Trend (Mean Estimate by Year)")
    mal_trend = mal_tab.groupby('year')['mean_estimate'].mean().reset_index()
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=mal_trend, x='year', y='mean_estimate', marker='o', ax=ax2)
    st.pyplot(fig2)

    # 3. Stacked Bar by Age Group
    st.subheader("Obesity Count by Year & Age Group")
    st_bar = obe_tab.groupby(["year", 'age_group']).agg({"gender": 'count'}).reset_index()
    pivot1 = st_bar.pivot(index="year", columns="age_group", values="gender")
    fig3, ax3 = plt.subplots(figsize=(15, 5))
    pivot1.plot(kind="bar", stacked=True, ax=ax3)
    st.pyplot(fig3)

    # 4. Pie Chart - Obesity Region
    st.subheader("Obesity by Region")
    regn = obe_tab.groupby('region')['mean_estimate'].mean()
    fig4, ax4 = plt.subplots()
    ax4.pie(regn.values, labels=regn.index, autopct="%1.2f%%")
    st.pyplot(fig4)

    # 5. Pie Chart - Malnutrition Region
    st.subheader("Malnutrition by Region")
    pie_mal = mal_tab.groupby('region')['mean_estimate'].mean()
    fig5, ax5 = plt.subplots()
    ax5.pie(pie_mal.values, labels=pie_mal.index, autopct="%1.2f%%")
    st.pyplot(fig5)

    # 6. Histogram
    st.subheader("Obesity Records by Year")
    fig6, ax6 = plt.subplots()
    sns.histplot(data=obe_tab, x="year", ax=ax6)
    st.pyplot(fig6)

    # 7. Obesity Level Bar
    st.subheader("Obesity Level by Year")
    ob_lvl = obe_tab.groupby(["year", 'obesity_level'])["gender"].count().reset_index()
    pivot2 = ob_lvl.pivot(index="year", columns="obesity_level", values="gender")
    fig7, ax7 = plt.subplots(figsize=(15, 5))
    pivot2.plot(kind="bar", stacked=True, ax=ax7)
    st.pyplot(fig7)

    # 8. Malnutrition Level Bar
    st.subheader("Malnutrition Level by Year")
    mal_lvl = mal_tab.groupby(["year", 'malnutrition_level'])["gender"].count().reset_index()
    pivot3 = mal_lvl.pivot(index="year", columns="malnutrition_level", values="gender")
    fig8, ax8 = plt.subplots(figsize=(15, 5))
    pivot3.plot(kind="bar", stacked=True, ax=ax8)
    st.pyplot(fig8)

    # 9. Pie Chart - Obesity by Country
    st.subheader("Top 10 Obese Countries")
    obe_coun = obe_tab.groupby('country')['mean_estimate'].mean().sort_values(ascending=False).head(10)
    fig9 = px.pie(values=obe_coun.values, names=obe_coun.index, hole=0.6)
    st.plotly_chart(fig9)

    # 10. Pie Chart - Malnutrition by Country
    st.subheader("Top 10 Malnourished Countries")
    mal_coun = mal_tab.groupby('country')['mean_estimate'].mean().sort_values(ascending=False).head(10)
    fig10 = px.pie(values=mal_coun.values, names=mal_coun.index, hole=0.6)
    st.plotly_chart(fig10)

# ----------------------------------------
# 5. 📄 Summary Tab
# ----------------------------------------
# 5. Summary Tab
with tabs[4]:
    st.header("📄 Summary of Key Insights")
    
    st.markdown("""
### 📊 Summary of Key Insights

---

#### 🔹 1. Global Trends Over Time
- **Obesity is increasing year by year**:
  - In **2012**, the global average obesity level was **11.0%**
  - By **2022**, it rose to **14.8%**

- **Malnutrition is gradually decreasing**:
  - In **2012**, the global average malnutrition level was **5.57%**
  - In **2022**, it decreased slightly to **5.20%**

---

#### 🔹 2. Age Group Comparison
- **Children have higher obesity levels** than adults.
- Indicates a **rising childhood obesity crisis**.

---

#### 🔹 3. Regional Analysis

📈 **Obesity**:
- **Western Pacific**: Highest obesity region (**26%**)
- **Americas**: Second most affected (**23%**)
- **Eastern Mediterranean**: Third in obesity prevalence

📉 **Malnutrition**:
- **South-East Asia**: Highest malnutrition (**36.64%**)
- **Africa**: Second (**22.8%**)
- **Eastern Mediterranean**: Also affected — both **overnutrition and undernutrition**

📌 **Insight**: Eastern Mediterranean is a **dual-burden region** needing critical intervention.

---

#### 🔹 4. Gender-Based Analysis
- **Females show higher average obesity** than males across most countries.
- Suggests **gender-specific intervention** for lifestyle and education.

---

#### 🔹 5. Country-Level Extremes

**Top 3 in Obesity**:
- Niue  
- Cook Islands  
- Nauru  

**Top 3 in Malnutrition**:
- India  
- South-East Asia (regional)  
- Bangladesh  

---

#### 🔹 6. Population Consistency
- Every year has **same population count (2520)** in dataset.
- Ensures **reliable year-over-year comparisons**.

---

#### 🔹 7. Obesity Levels Categorized
- **Low-level obesity** most common but declining.
- **High-level obesity** rising each year – a **warning signal**.

---

### 🩺 Recommendations

✅ **1. Focus on Dual-Burden Regions**
- Especially **Eastern Mediterranean**
- Improve **balanced diets**
- Combat both **hunger and obesity**

✅ **2. Target High-Risk Countries**
- Obesity: **Niue, Cook Islands, Nauru**
- Malnutrition: **India, Bangladesh, South-East Asia**

✅ **3. Child-Focused Programs**
- Launch **school nutrition + fitness** programs
- Educate **parents on early health habits**

✅ **4. Gender-Specific Awareness**
- Create tailored **diet & lifestyle programs** for women

✅ **5. Monitor and Reduce CI Width**
- Invest in **better data quality**, especially in under-reported regions

✅ **6. Policy Actions**
- **Tax sugary/junk foods**
- Promote **local, traditional diets**
- Strengthen **maternal nutrition policies**
    """)

