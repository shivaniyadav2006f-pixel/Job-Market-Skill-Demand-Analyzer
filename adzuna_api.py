import requests
import pandas as pd
import streamlit as st
import re


# =========================================================
# ADZUNA API SETTINGS
# =========================================================

BASE_URL = (
    "https://api.adzuna.com/v1/api/jobs/in/search/1"
)


# =========================================================
# TEXT HELPER
# =========================================================

def clean_text(value):

    if value is None:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(value)
    ).strip().lower()


# =========================================================
# API CREDENTIALS
# =========================================================

def get_api_credentials():

    try:

        app_id = st.secrets["adzuna"]["app_id"]
        app_key = st.secrets["adzuna"]["app_key"]

    except Exception:

        return None, None

    if not app_id or not app_key:

        return None, None

    return (
        str(app_id).strip(),
        str(app_key).strip()
    )


# =========================================================
# JOB ROLE MATCHING
# =========================================================

def role_matches(
    job_title,
    description,
    selected_role
):

    role = clean_text(
        selected_role
    )

    title = clean_text(
        job_title
    )

    description = clean_text(
        description
    )

    if not role:
        return True

    text = f"{title} {description}"

    role_aliases = {

        "ai engineer": [
            "ai engineer",
            "artificial intelligence engineer",
            "machine learning engineer",
            "ml engineer",
            "ai developer"
        ],

        "data scientist": [
            "data scientist",
            "data science"
        ],

        "data analyst": [
            "data analyst",
            "data analytics"
        ],

        "data engineer": [
            "data engineer",
            "data engineering"
        ],

        "business analyst": [
            "business analyst",
            "business analysis"
        ],

        "python developer": [
            "python developer",
            "python development"
        ],

        "software developer": [
            "software developer",
            "software engineer",
            "application developer"
        ],

        "software engineer": [
            "software engineer",
            "software developer",
            "application engineer"
        ],

        "web developer": [
            "web developer",
            "web development",
            "frontend developer",
            "backend developer",
            "full stack developer"
        ],

        "machine learning engineer": [
            "machine learning engineer",
            "ml engineer",
            "machine learning"
        ],

        "cloud engineer": [
            "cloud engineer",
            "cloud computing",
            "aws engineer",
            "azure engineer"
        ],

        "devops engineer": [
            "devops engineer",
            "devops",
            "site reliability engineer",
            "sre"
        ],

        "cybersecurity analyst": [
            "cybersecurity analyst",
            "cyber security analyst",
            "security analyst",
            "information security analyst",
            "soc analyst"
        ],

        "qa engineer": [
            "qa engineer",
            "quality assurance engineer",
            "test engineer",
            "software tester"
        ],

        "frontend developer": [
            "frontend developer",
            "front end developer",
            "ui developer"
        ],

        "backend developer": [
            "backend developer",
            "back end developer"
        ],

        "full stack developer": [
            "full stack developer",
            "fullstack developer"
        ],

        "java developer": [
            "java developer",
            "java engineer"
        ],

        "mobile app developer": [
            "mobile app developer",
            "android developer",
            "ios developer"
        ],

        "database administrator": [
            "database administrator",
            "database admin",
            "dba"
        ],

        "system administrator": [
            "system administrator",
            "systems administrator",
            "system admin"
        ],

        "network engineer": [
            "network engineer",
            "networking engineer"
        ],

        "technical support engineer": [
            "technical support engineer",
            "technical support"
        ],

        "product manager": [
            "product manager",
            "product management"
        ],

        "project manager": [
            "project manager",
            "project management"
        ],

        "ui/ux designer": [
            "ui/ux designer",
            "ui ux designer",
            "ux designer",
            "ui designer"
        ],

        "ux designer": [
            "ux designer",
            "user experience designer"
        ],

        "graphic designer": [
            "graphic designer",
            "graphic design"
        ]
    }

    aliases = role_aliases.get(
        role,
        [role]
    )

    return any(
        alias in text
        for alias in aliases
    )


# =========================================================
# LOCATION MATCHING
# =========================================================

def location_matches(
    job_location,
    selected_location
):

    location = clean_text(
        selected_location
    )

    job_location = clean_text(
        job_location
    )

    if (
        not location
        or location == "all india"
    ):
        return True

    # -----------------------------------------------------
    # LOCALITY ALIASES
    # -----------------------------------------------------

    locality_aliases = {

        "andheri": [
            "andheri"
        ],

        "borivali": [
            "borivali"
        ],

        "bandra": [
            "bandra"
        ],

        "powai": [
            "powai"
        ],

        "goregaon": [
            "goregaon"
        ],

        "malad": [
            "malad"
        ],

        "thane": [
            "thane"
        ],

        "kalyan": [
            "kalyan"
        ],

        "dombivli": [
            "dombivli"
        ],

        "navi mumbai": [
            "navi mumbai"
        ],

        "hinjewadi": [
            "hinjewadi"
        ],

        "kharadi": [
            "kharadi"
        ],

        "wakad": [
            "wakad"
        ],

        "viman nagar": [
            "viman nagar"
        ],

        "hadapsar": [
            "hadapsar"
        ],

        "whitefield": [
            "whitefield"
        ],

        "electronic city": [
            "electronic city"
        ],

        "koramangala": [
            "koramangala"
        ],

        "marathahalli": [
            "marathahalli"
        ],

        "hitech city": [
            "hitech city"
        ],

        "gachibowli": [
            "gachibowli"
        ],

        "madhapur": [
            "madhapur"
        ]
    }

    if location in locality_aliases:

        return any(
            alias in job_location
            for alias in locality_aliases[location]
        )

    # -----------------------------------------------------
    # CITY ALIASES
    # -----------------------------------------------------

    city_aliases = {

        "mumbai": [
            "mumbai",
            "bombay"
        ],

        "pune": [
            "pune"
        ],

        "bengaluru": [
            "bengaluru",
            "bangalore"
        ],

        "delhi": [
            "delhi",
            "new delhi"
        ],

        "noida": [
            "noida"
        ],

        "greater noida": [
            "greater noida"
        ],

        "gurugram": [
            "gurugram",
            "gurgaon"
        ],

        "ghaziabad": [
            "ghaziabad"
        ],

        "faridabad": [
            "faridabad"
        ],

        "hyderabad": [
            "hyderabad"
        ]
    }

    aliases = city_aliases.get(
        location,
        [location]
    )

    return any(
        alias in job_location
        for alias in aliases
    )


# =========================================================
# EXPERIENCE MATCHING
# =========================================================

def experience_matches(
    job_title,
    description,
    selected_experience
):

    experience = clean_text(
        selected_experience
    )

    if not experience:
        return True

    text = clean_text(
        f"{job_title} {description}"
    )

    # -----------------------------------------------------
    # FRESHER
    # -----------------------------------------------------

    if experience == "fresher":

        fresher_terms = [

            "fresher",
            "freshers",
            "entry level",
            "entry-level",
            "graduate",
            "graduates",
            "no experience",
            "without experience",
            "0 years",
            "0-1 years",
            "0 - 1 years",
            "junior",
            "trainee"
        ]

        return any(
            term in text
            for term in fresher_terms
        )

    # -----------------------------------------------------
    # NORMALIZE EXPERIENCE
    # -----------------------------------------------------

    if not experience:
        return True

    text = clean_text(text)
    experience = clean_text(experience)

    compact_text = text.replace(" ", "")
    compact_experience = experience.replace(" ", "")

    if compact_experience in compact_text:
        return True

    # -----------------------------------------------------
    # EXPERIENCE RANGE
    # -----------------------------------------------------

    range_match = re.match(
        r"(\d+)\s*-\s*(\d+)\s*years?",
        experience
    )

    if range_match:

        start = range_match.group(1)
        end = range_match.group(2)

        patterns = [

            f"{start}-{end} years",
            f"{start} - {end} years",
            f"{start} to {end} years",
            f"{start}+ years",
            f"{start} years",
            f"{end} years"
        ]

        return any(
            pattern in text
            for pattern in patterns
        )

    # -----------------------------------------------------
    # PLUS EXPERIENCE
    # -----------------------------------------------------

    plus_match = re.match(
        r"(\d+)\+\s*years?",
        experience
    )

    if plus_match:

        number = plus_match.group(1)

        patterns = [

            f"{number}+ years",
            f"{number} years",
            f"{number} years of experience"
        ]

        return any(
            pattern in text
            for pattern in patterns
        )

    # -----------------------------------------------------
    # SINGLE YEAR
    # -----------------------------------------------------

    single_match = re.match(
        r"(\d+)\s*years?",
        experience
    )

    if single_match:

        number = single_match.group(1)

        patterns = [

            f"{number} years",
            f"{number}-1 years",
            f"{number} - 1 years",
            f"{number}+ years",
            f"{number} year"
        ]

        return any(
            pattern in text
            for pattern in patterns
        )

    return False


# =========================================================
# FETCH LIVE JOBS FROM ADZUNA
# =========================================================

def fetch_live_jobs(
    job_role="",
    location="",
    experience="",
    results_per_page=50
):

    # -----------------------------------------------------
    # API CREDENTIALS
    # -----------------------------------------------------

    app_id, app_key = get_api_credentials()

    if not app_id or not app_key:

        return (

            pd.DataFrame(),

            "❌ Adzuna API credentials were not found. "
            "Check .streamlit/secrets.toml."
        )

    # -----------------------------------------------------
    # API PARAMETERS
    # -----------------------------------------------------

    params = {

        "app_id": app_id,

        "app_key": app_key,

        "results_per_page": results_per_page,

        "content-type": "application/json"
    }

    # -----------------------------------------------------
    # JOB ROLE
    # -----------------------------------------------------

    if job_role:

        params["what"] = job_role

    # -----------------------------------------------------
    # LOCATION
    # -----------------------------------------------------

    if (
        location
        and clean_text(location) != "all india"
    ):

        params["where"] = location

    # -----------------------------------------------------
    # API REQUEST
    # -----------------------------------------------------

    try:

        response = requests.get(

            BASE_URL,

            params=params,

            timeout=20
        )

        if response.status_code != 200:

            return (

                pd.DataFrame(),

                f"❌ Adzuna API error: "
                f"{response.status_code} - "
                f"{response.text[:300]}"
            )

        data = response.json()

    except requests.exceptions.Timeout:

        return (

            pd.DataFrame(),

            "❌ Adzuna API request timed out. "
            "Please try again."
        )

    except requests.exceptions.RequestException as e:

        return (

            pd.DataFrame(),

            f"❌ Unable to connect to Adzuna API: {e}"
        )

    except ValueError:

        return (

            pd.DataFrame(),

            "❌ Adzuna returned an invalid response."
        )

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    results = data.get(
        "results",
        []
    )

    if not results:

        return (
            pd.DataFrame(),
            None
        )

    # -----------------------------------------------------
    # RESULT STORAGE
    # -----------------------------------------------------

    exact_rows = []

    fallback_rows = []

    # -----------------------------------------------------
    # PROCESS EACH JOB
    # -----------------------------------------------------

    for item in results:

        # =================================================
        # JOB TITLE
        # =================================================

        title = item.get(
            "title",
            "Not Available"
        )

        # =================================================
        # COMPANY
        # =================================================

        company_data = item.get(
            "company",
            {}
        )

        if isinstance(
            company_data,
            dict
        ):

            company = company_data.get(
                "display_name",
                "Not Available"
            )

        else:

            company = str(
                company_data
            )

        # =================================================
        # LOCATION
        # =================================================

        location_data = item.get(
            "location",
            {}
        )

        if isinstance(
            location_data,
            dict
        ):

            display_location = location_data.get(
                "display_name",
                "Not Available"
            )

        else:

            display_location = str(
                location_data
            )

        # =================================================
        # DESCRIPTION
        # =================================================

        description = item.get(
            "description",
            ""
        )

        # =================================================
        # ROLE FILTER
        # =================================================

        if not role_matches(

            title,

            description,

            job_role
        ):

            continue

        # =================================================
        # LOCATION FILTER
        # =================================================

        if not location_matches(

            display_location,

            location
        ):

            continue

        # =================================================
        # JOB ROW
        # =================================================

        row = {

            "Job Title": title,

            "Company": company,

            "Location": display_location,

            "Salary Min": item.get(
                "salary_min"
            ),

            "Salary Max": item.get(
                "salary_max"
            ),

            "Job Type": item.get(
                "contract_type",
                "Not Available"
            ),

            "Job Time": item.get(
                "contract_time",
                "Not Available"
            ),

            "Description": description,

            "Apply URL": item.get(
                "redirect_url",
                ""
            )
        }

        # =================================================
        # FALLBACK RESULT
        # =================================================

        fallback_rows.append(
            row
        )

        # =================================================
        # EXPERIENCE FILTER
        # =================================================

        if experience:

            if experience_matches(

                title,

                description,

                experience
            ):

                exact_rows.append(
                    row
                )

        else:

            exact_rows.append(
                row
            )

    # =====================================================
    # EXACT EXPERIENCE RESULTS
    # =====================================================

    if exact_rows:

        return (

            pd.DataFrame(
                exact_rows
            ),

            None
        )

    # =====================================================
    # EXPERIENCE FALLBACK
    # =====================================================

    if fallback_rows:

        return (

            pd.DataFrame(
                fallback_rows
            ),

            None
        )

    # =====================================================
    # NO RESULTS
    # =====================================================

    return (

        pd.DataFrame(),

        None
    )