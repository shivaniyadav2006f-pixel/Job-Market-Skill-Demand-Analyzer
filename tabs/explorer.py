import streamlit as st


def explorer_tab(filtered_df):

    st.subheader(
        "📄 Job Data Explorer"
    )

    st.write(
        f"Showing **{len(filtered_df):,}** filtered records."
    )

    st.dataframe(
        filtered_df.head(200),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Job Data",
        data=csv_data,
        file_name="filtered_job_market.csv",
        mime="text/csv",
        use_container_width=True
    )