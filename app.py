import streamlit as st
import pandas as pd
import plotly.express as px

from pathlib import Path
from dotenv import load_dotenv

import os
import google.generativeai as genai



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="AI Business Insight Generator",

    page_icon="📊",

    layout="wide"

)



# ============================================================
# GEMINI CONFIGURATION
# ============================================================

load_dotenv()


API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not API_KEY:

    st.error(
        "Gemini API Key not found."
    )

    st.stop()



genai.configure(

    api_key=API_KEY

)



model = genai.GenerativeModel(

    "models/gemini-3.1-flash-lite"

)



# ============================================================
# BUSINESS RULES
# ============================================================


def load_business_rules():


    rule_path = Path(
        "knowledge/business_rules.txt"
    )


    if rule_path.exists():


        with open(

            rule_path,

            "r",

            encoding="utf-8"

        ) as f:


            return f.read()


    return "Business Rules Not Found."





# ============================================================
# HEADER
# ============================================================


st.title(
    "📊 AI Business Insight Generator"
)



st.write(

    "Generate AI powered business insights from business datasets using Gemini + RAG."

)



st.divider()



# ============================================================
# FILE UPLOAD
# ============================================================


uploaded_file = st.file_uploader(

    "Upload Business CSV Dataset",

    type=["csv"],

    key="business_dataset_upload"

)



# ============================================================
# LOAD DATA
# ============================================================


if uploaded_file:


    try:


        df = pd.read_csv(

            uploaded_file

        )


    except:


        df = pd.read_csv(

            uploaded_file,

            encoding="latin1"

        )



    st.success(

        "Dataset Loaded Successfully ✅"

    )



    st.divider()



    # ========================================================
    # DATA PREVIEW
    # ========================================================


    with st.expander(

        "📄 Dataset Preview"

    ):


        st.dataframe(

            df.head(20),

            use_container_width=True

        )



    # ========================================================
    # KPI CALCULATION
    # ========================================================


    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    required_columns = [
        "Sales",
        "Profit",
        "Order ID",
        "Customer ID",
        "Discount",
        "Category",
        "Region",
        "Segment",
    ]
    column_lookup = {column.casefold(): column for column in df.columns}
    df = df.rename(
        columns={
            column_lookup[required.casefold()]: required
            for required in required_columns
            if required.casefold() in column_lookup
            and column_lookup[required.casefold()] != required
        }
    )

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]
    if missing_columns:
        st.error(
            "The uploaded CSV is missing required columns: "
            + ", ".join(missing_columns)
        )
        st.info(
            "Available columns: "
            + ", ".join(str(column) for column in df.columns)
        )
        st.stop()


    total_sales = df["Sales"].sum()


    total_profit = df["Profit"].sum()


    total_orders = df["Order ID"].nunique()


    total_customers = df["Customer ID"].nunique()


    avg_discount = df["Discount"].mean() * 100
        # ========================================================
    # KPI CARDS
    # ========================================================


    col1, col2, col3, col4, col5 = st.columns(5)



    col1.metric(

        "💰 Total Sales",

        f"${total_sales:,.0f}"

    )



    col2.metric(

        "💵 Total Profit",

        f"${total_profit:,.0f}"

    )



    col3.metric(

        "📦 Orders",

        total_orders

    )



    col4.metric(

        "👥 Customers",

        total_customers

    )



    col5.metric(

        "🏷 Average Discount",

        f"{avg_discount:.1f}%"

    )



    st.divider()



    # ========================================================
    # BUSINESS SUMMARY TABLES
    # ========================================================


    category_sales = (

        df.groupby("Category")["Sales"]

        .sum()

        .reset_index()

    )



    region_profit = (

        df.groupby("Region")["Profit"]

        .sum()

        .reset_index()

    )



    segment_sales = (

        df.groupby("Segment")["Sales"]

        .sum()

        .reset_index()

    )



    # ========================================================
    # BUSINESS INSIGHTS
    # ========================================================


    top_category = (

        category_sales

        .sort_values(

            "Sales",

            ascending=False

        )

        .iloc[0]["Category"]

    )



    lowest_category = (

        category_sales

        .sort_values(

            "Sales",

            ascending=True

        )

        .iloc[0]["Category"]

    )



    best_region = (

        region_profit

        .sort_values(

            "Profit",

            ascending=False

        )

        .iloc[0]["Region"]

    )



    worst_region = (

        region_profit

        .sort_values(

            "Profit",

            ascending=True

        )

        .iloc[0]["Region"]

    )



    # ========================================================
    # DASHBOARD CHARTS
    # ========================================================


    st.subheader(

        "📈 Business Dashboard"

    )



    chart1, chart2 = st.columns(2)



    with chart1:


        fig = px.bar(

            category_sales,

            x="Category",

            y="Sales",

            title="Sales by Category",

            text_auto=True

        )



        st.plotly_chart(

            fig,

            use_container_width=True

        )



    with chart2:


        fig2 = px.bar(

            region_profit,

            x="Region",

            y="Profit",

            title="Profit by Region",

            text_auto=True

        )



        st.plotly_chart(

            fig2,

            use_container_width=True

        )



    st.divider()



    fig3 = px.pie(

        segment_sales,

        names="Segment",

        values="Sales",

        title="Sales by Segment"

    )



    st.plotly_chart(

        fig3,

        use_container_width=True

    )



    st.divider()
        # ========================================================
    # AI BUSINESS QUESTION
    # ========================================================


    st.subheader(

        "🤖 Ask Your Business Question"

    )



    user_question = st.text_input(

        "",

        placeholder="Example: Why sales dropped last month?"

    )



    # ========================================================
    # BUSINESS RULES
    # ========================================================


    business_rules = load_business_rules()



    # ========================================================
    # RAG CONTEXT
    # ========================================================


    kpi_summary = f"""

BUSINESS KPI SUMMARY


Total Sales:

${total_sales:,.2f}


Total Profit:

${total_profit:,.2f}


Total Orders:

{total_orders}


Total Customers:

{total_customers}


Average Discount:

{avg_discount:.2f}%


Top Category:

{top_category}


Lowest Category:

{lowest_category}


Best Region:

{best_region}


Worst Region:

{worst_region}


"""



    # ========================================================
    # GEMINI PROMPT
    # ========================================================


    prompt = f"""

You are an experienced Business Intelligence Consultant.


Business Rules:

{business_rules}



Business KPI Summary:

{kpi_summary}



User Question:

{user_question}



Analyze the business data and provide:


# Executive Summary


# Key Insights


# Possible Reasons


# Risks


# Opportunities


# Recommendations


# Business Health Score


Use emojis.

Keep response within 300 words.

Return markdown format.

"""



    # ========================================================
    # GENERATE AI INSIGHTS
    # ========================================================


    if st.button(

        "🚀 Generate AI Insights",

        key="generate_ai_insight"

    ):


        if user_question.strip() == "":


            st.warning(

                "Please enter your business question."

            )


        else:


            try:


                with st.spinner(

                    "🤖 Gemini is analysing your business data..."

                ):


                    response = model.generate_content(

                        prompt

                    )



                ai_output = response.text



                st.success(
                    "✅ Analysis Completed"

                )



                st.divider()



                # ============================================
                # AI RESPONSE
                # ============================================


                st.markdown(

                    """
                    <div style='background:#E3F2FD;
                    padding:20px;
                    border-radius:12px;'>

                    <h2>🤖 AI Business Insights</h2>

                    </div>
                    """,

                    unsafe_allow_html=True

                )



                st.markdown(

                    ai_output

                )



                st.divider()



                # ============================================
                # BUSINESS HEALTH SCORE
                # ============================================


                score = 100



                if avg_discount > 20:

                    score -= 10



                if total_profit < 0:

                    score -= 40



                if total_sales < 100000:

                    score -= 20



                if score >= 85:

                    health = "🟢 Excellent"



                elif score >= 70:

                    health = "🟡 Good"



                elif score >= 50:

                    health = "🟠 Average"



                else:

                    health = "🔴 Critical"



                st.subheader(

                    "⭐ Business Health Score"

                )



                score1, score2 = st.columns(2)



                score1.metric(

                    "Overall Score",

                    f"{score}/100"

                )



                score2.metric(

                    "Business Status",

                    health

                )



                st.progress(

                    score/100

                )



                st.divider()
                                # ============================================
                # QUICK BUSINESS INSIGHTS
                # ============================================


                st.subheader(

                    "📌 Quick Business Summary"

                )



                c1, c2 = st.columns(2)



                with c1:


                    st.info(

                        f"""

🏆 Top Category


**{top_category}**

"""

                    )



                    st.success(

                        f"""

🌍 Best Region


**{best_region}**

"""

                    )



                with c2:


                    st.warning(

                        f"""

📉 Lowest Category


**{lowest_category}**

"""

                    )



                    st.error(

                        f"""

⚠ Lowest Profit Region


**{worst_region}**

"""

                    )



                st.divider()



                # ============================================
                # DOWNLOAD AI REPORT
                # ============================================


                report = f"""

AI BUSINESS INSIGHT REPORT

================================


BUSINESS KPIs

--------------------------------


Total Sales:

${total_sales:,.2f}


Total Profit:

${total_profit:,.2f}


Total Orders:

{total_orders}


Total Customers:

{total_customers}


Average Discount:

{avg_discount:.2f}%



BUSINESS PERFORMANCE

--------------------------------


Top Category:

{top_category}


Lowest Category:

{lowest_category}


Best Region:

{best_region}


Worst Region:

{worst_region}



BUSINESS HEALTH

--------------------------------


Score:

{score}/100


Status:

{health}



AI GENERATED INSIGHTS

--------------------------------


{ai_output}



================================

Generated using AI Business Insight Generator

"""



                st.download_button(

                    label="📥 Download AI Report",

                    data=report,

                    file_name="AI_Business_Insight_Report.txt",

                    mime="text/plain"

                )



            except Exception as e:


                st.error(

                    f"Error while generating AI insights: {e}"

                )