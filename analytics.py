import re
import pandas as pd

from data_loader import find_column, get_skill_column


# =========================================================
# SKILL COUNTS
# =========================================================

def get_skill_counts(df):

    skill_column = get_skill_column(df)

    if skill_column is None:
        return pd.Series(dtype=int)

    counter = {}

    for value in df[skill_column].dropna():

        skills = str(value).split(",")

        unique_skills = set()

        for skill in skills:

            cleaned = skill.strip()

            if cleaned:
                unique_skills.add(cleaned.lower())

        for skill in unique_skills:

            display_skill = skill.title()

            counter[display_skill] = (
                counter.get(display_skill, 0) + 1
            )

    if not counter:
        return pd.Series(dtype=int)

    return pd.Series(counter).sort_values(
        ascending=False
    )


# =========================================================
# ROLE COUNTS
# =========================================================

def get_role_counts(df):

    role_column = find_column(
        df,
        [
            "Job Role",
            "Job Title",
            "Role",
            "Title",
            "Position",
            "Job"
        ]
    )

    if role_column is None:
        return pd.Series(dtype=int)

    return (
        df[role_column]
        .dropna()
        .astype(str)
        .str.strip()
        .value_counts()
    )


# =========================================================
# SALARY COLUMN
# =========================================================

def get_salary_column(df):

    return find_column(
        df,
        [
            "Salary",
            "Salary Range",
            "Annual Salary",
            "Average Salary",
            "Salary (USD)",
            "Salary INR",
            "Salary Range (USD)"
        ]
    )


# =========================================================
# SALARY EXTRACTION
# =========================================================

def extract_salary(value):

    if pd.isna(value):
        return None

    text = str(value)

    numbers = re.findall(
        r"\d+(?:,\d+)*(?:\.\d+)?",
        text
    )

    if not numbers:
        return None

    values = []

    for number in numbers:

        try:

            values.append(
                float(number.replace(",", ""))
            )

        except ValueError:
            pass

    if not values:
        return None

    # If salary is a range, use average
    return sum(values) / len(values)