import streamlit as st
import pandas as pd
import re


def salary_tab(filtered_df, role_column):

    st.subheader("💰 Salary Intelligence")

    # Find Salary column
    salary_column = None

    for col in filtered_df.columns:
        if str(col).strip().lower() == "salary":
            salary_column = col
            break

    if salary_column is None:
        st.warning("⚠️ Salary column not found in the dataset.")
        return

    # Copy required data
    salary_data = filtered_df[[role_column, salary_column]].copy()

    salary_data.columns = ["Job Role", "Salary"]

    salary_data = salary_data.dropna(subset=["Salary"])

    if salary_data.empty:
        st.warning("⚠️ No salary data available for the selected filters.")
        return

    # Convert salary range into minimum and maximum LPA
    def extract_salary(value):

        numbers = re.findall(r"\d+(?:\.\d+)?", str(value))

        if len(numbers) >= 2:
            return float(numbers[0]), float(numbers[1])

        elif len(numbers) == 1:
            number = float(numbers[0])
            return number, number

        return None, None

    salary_data[["Min Salary", "Max Salary"]] = salary_data["Salary"].apply(
        lambda x: pd.Series(extract_salary(x))
    )

    salary_data = salary_data.dropna(
        subset=["Min Salary", "Max Salary"]
    )

    if salary_data.empty:
        st.warning("⚠️ Salary values could not be processed.")
        return

    # Average salary
    salary_data["Average Salary"] = (
        salary_data["Min Salary"] + salary_data["Max Salary"]
    ) / 2

    # --------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💰 Minimum Salary",
            f"{salary_data['Min Salary'].min():.1f} LPA"
        )

    with col2:
        st.metric(
            "💰 Maximum Salary",
            f"{salary_data['Max Salary'].max():.1f} LPA"
        )

    with col3:
        st.metric(
            "📊 Average Salary",
            f"{salary_data['Average Salary'].mean():.1f} LPA"
        )

    st.divider()

    # --------------------------------------------------
    # ROLE-WISE SALARY
    # --------------------------------------------------

    st.subheader("📊 Salary by Job Role")

    role_salary = (
        salary_data
        .groupby("Job Role")["Average Salary"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(role_salary)

    st.divider()

    # --------------------------------------------------
    # SALARY DETAILS TABLE
    # --------------------------------------------------

    st.subheader("📋 Salary Details")

    display_data = salary_data[
        ["Job Role", "Salary", "Min Salary", "Max Salary", "Average Salary"]
    ].copy()

    display_data["Min Salary"] = display_data["Min Salary"].map(
        lambda x: f"{x:.1f} LPA"
    )

    display_data["Max Salary"] = display_data["Max Salary"].map(
        lambda x: f"{x:.1f} LPA"
    )

    display_data["Average Salary"] = display_data["Average Salary"].map(
        lambda x: f"{x:.1f} LPA"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )