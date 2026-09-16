import streamlit as st
import pandas as pd


@st.cache_data
def load_data():

    try:
        df = pd.read_csv("job_market.csv")

        df = df.dropna(how="all")

        df.columns = [
            str(column).strip()
            for column in df.columns
        ]

        return df

    except FileNotFoundError:
        return None

    except Exception as error:
        st.error(
            f"Unable to load dataset: {error}"
        )
        return None


def find_column(df, possible_names):

    if df is None:
        return None

    normalized = {}

    for column in df.columns:

        clean = (
            str(column)
            .strip()
            .lower()
            .replace("_", " ")
        )

        normalized[clean] = column

    for name in possible_names:

        clean_name = (
            name
            .strip()
            .lower()
            .replace("_", " ")
        )

        if clean_name in normalized:
            return normalized[clean_name]

    return None


def get_skill_column(df):

    return find_column(
        df,
        [
            "Skills",
            "Skill",
            "Required Skills",
            "Job Skills",
            "Required Skill",
            "Technical Skills"
        ]
    )